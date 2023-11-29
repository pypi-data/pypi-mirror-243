from __future__ import annotations
from io import IOBase
import logging
from pathlib import Path
from typing import Any, Sequence, TypeVar, Generic
from urllib.parse import quote
from ..text import hide_url_password, skip_bom, build_url

logger = logging.getLogger(__name__)

T_Connection = TypeVar('T_Connection')
T_Cursor = TypeVar('T_Cursor')
T_Composable = TypeVar('T_Composable')
T_Composed = TypeVar('T_Composed')


class DbAdapter(Generic[T_Connection, T_Cursor, T_Composable, T_Composed]):
    URL_SCHEME: str
    DEFAULT_SCHEMA = None
    ONLY_POSITIONAL_PARAMS = False
    EXPECTED_CONNECTION_TYPES: list[str]

    @classmethod
    def is_available(cls):
        raise NotImplementedError()
    

    def __init__(self, origin: T_Connection|str|dict, autocommit: bool = True):
        """
        Create a new adapter.
        - `origin`: an existing connection object, or the URL or django alias (e.g. 'default') for the new connection to create by the adapter.
        - `autocommit`: whether or not to auto-commit transactions (applies only for connections created by the adapter)
        """
        if not self.is_available():
            raise ValueError(f"cannot use {type(self).__name__} (not available)")
        
        if isinstance(origin, str):
            self._must_close_connection = True
            self._connection: T_Connection = None
            if ':' in origin or '/' in origin or ';' in origin or ' ' in origin:
                self._connection_url = origin
            else:
                from django.conf import settings
                if not origin in settings.DATABASES:
                    raise ValueError(f"key \"{origin}\" not found in django DATABASES settings")
                config: dict[str,Any] = settings.DATABASES[origin]
                
                build_url(
                    scheme = self.URL_SCHEME,
                    hostname = config.get('HOST', None),
                    port = config.get('PORT', None),
                    username = config.get('USER', None),
                    password = config.get('PASSWORD', None),
                    path = config.get('NAME', None),
                )

        elif isinstance(origin, dict):
            self._must_close_connection = True
            self._connection: T_Connection = None

            if 'NAME' in origin:
                # uppercase (as used by django)
                self._connection_url = build_url(
                    scheme = self.URL_SCHEME,
                    hostname = origin.get('HOST', None),
                    port = origin.get('PORT', None),
                    username = origin.get('USER', None),
                    password = origin.get('PASSWORD', None),
                    path = origin.get('NAME', None),
                )

            else:
                # lowercase (as used by some drivers' connection kwargs)
                self._connection_url = build_url(
                    scheme = self.URL_SCHEME,
                    hostname = origin.get('host', None),
                    port = origin.get('port', None),
                    username = origin.get('user', None),
                    password = origin.get('password', None),
                    path = origin.get('name', origin.get('dbname', None)),
                )

        else:
            origin = _get_connection_from_wrapper(origin)

            fulltype = type(origin).__module__ + '.' + type(origin).__qualname__
            if fulltype not in self.EXPECTED_CONNECTION_TYPES:
                raise ValueError(f"invalid connection type for {type(self).__name__}: {fulltype}")
            self._connection = origin
            self._connection_url: str = None
            self._must_close_connection = False
        
        self._autocommit: bool = autocommit


    def __enter__(self):
        return self


    def __exit__(self, exc_type = None, exc_val = None, exc_tb = None):
        if self._connection and self._must_close_connection:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"close %s (%s) connection to %s", type(self).__name__, type(self._connection).__module__ + '.' + type(self._connection).__qualname__, hide_url_password(self._connection_url))
            self._connection.close()


    @property
    def connection(self):
        if not self._connection:                
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"create %s connection to %s", type(self).__name__, hide_url_password(self._connection_url))
            self._connection = self._create_connection()
        return self._connection


    def cursor(self) -> T_Cursor:
        return self.connection.cursor()


    def _create_connection(self) -> T_Connection:
        raise NotImplementedError()


    def get_url(self, table: str|tuple = None, *, with_password = False):
        if self._connection_url:
            url = self._connection_url
        else:
            url = self._get_url_from_connection()

        if with_password:
            url = hide_url_password(url)

        if table:
            schema, table = self.split_name(table)
            if table:
                url += f"/"
                if schema:
                    url += quote(schema)
                    url += '.'
                url += quote(table)

        return url


    def _get_url_from_connection(self):
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    # Execution
    #

    def execute(self, query: str, params: list|tuple|dict = None, limit: int = None):
        """
        Does not have to be closed.
        """
        with self.execute_get_cursor(query, params, limit=limit):
            pass
    

    def execute_get_cursor(self, query: str, params: list|tuple|dict = None, limit: int = None) -> T_Cursor:
        """
        Must be closed.
        """
        # Example of positional param: cursor.execute("INSERT INTO foo VALUES (%s)", ["bar"])
        # Example of named param: cursor.execute("INSERT INTO foo VALUES (%(foo)s)", {"foo": "bar"})
        if limit is not None:
            query = self.limit_query(query, limit=limit)
        
        if params is None:
            params = []
        elif isinstance(params, dict) and self.ONLY_POSITIONAL_PARAMS:
            query, params = self.to_positional_params(query, params)

        cursor = self.cursor()
        cursor.execute(query, params)
        return cursor


    def execute_get_scalar(self, query: str, params: list|tuple|dict = None, limit: int = None):
        with self.execute_get_cursor(query, params, limit=limit) as cursor:
            return self.get_scalar_from_cursor(cursor)


    def execute_file(self, path: str|Path, params: list|tuple|dict = None, limit: int = None, encoding: str = 'utf-8') -> None:
        with open(path, 'r', encoding=encoding) as fp:
            skip_bom(fp)
            query = fp.read()
            
        self.execute(query, params, limit=limit)
    

    def execute_procedure(self, name: str|tuple, *args) -> T_Cursor:
        return NotImplementedError()


    def get_scalar_from_cursor(self, cursor: T_Cursor) -> Any:
        generator = iter(cursor)
        result = next(generator)
        
        # Check only one row
        try:
            next(generator)
            raise ValueError(f"several rows returned by query")
        except StopIteration:
            pass

        # Check only one value
        if len(result) > 1:
            raise ValueError("several values returned by query")

        return result[0]


    # -------------------------------------------------------------------------
    # Queries
    #

    def to_positional_params(self, query: str, params: dict) -> tuple[str, Sequence[Any]]:
        from sqlparams import SQLParams  # not at the top because the enduser might not need this feature

        if not hasattr(self.__class__, '_params_formatter'):
            self.__class__._params_formatter = SQLParams('named', 'qmark')
        query, params = self.__class__._params_formatter.format(query, params)

        return query, params
    
    
    def limit_query(self, query: str, limit: int) -> str:
        if limit is None:
            return query
    
        if not isinstance(limit, int):
            raise ValueError(f"invalid type for limit: {type(limit).__name__} (expected int)")
        
        import sqlparse  # not at the top because the enduser might not need this feature

        # Parse SQL to remove token before the SELECT keyword
        # example: WITH (CTE) tokens
        statements = sqlparse.parse(query)
        if len(statements) != 1:
            raise ValueError(f"query contains {len(statements)} statements")

        # Get first DML keyword
        dml_keyword = None
        dml_keyword_index = None
        order_by_index = None
        for i, token in enumerate(statements[0].tokens):
            if token.ttype == sqlparse.tokens.DML:
                if dml_keyword is None:
                    dml_keyword = str(token).upper()
                    dml_keyword_index = i
            elif token.ttype == sqlparse.tokens.Keyword:
                if order_by_index is None:
                    keyword = str(token).upper()
                    if keyword == "ORDER BY":
                        order_by_index = i

        # Check if the DML keyword is SELECT
        if not dml_keyword:
            raise ValueError(f"no SELECT found (query does not contain DML keyword)")
        if dml_keyword != 'SELECT':
            raise ValueError(f"first DML keyword is {dml_keyword}, expected SELECT")

        # Get part before SELECT (example: WITH)
        if dml_keyword_index > 0:
            tokens = statements[0].tokens[:dml_keyword_index]
            limited_query = ''.join(str(token) for token in tokens)
        else:
            limited_query = ''
    
        # Append SELECT before ORDER BY
        if order_by_index is not None:
            tokens = statements[0].tokens[dml_keyword_index:order_by_index]
        else:
            tokens = statements[0].tokens[dml_keyword_index:]

        limited_query += self._limit_parsed_query(''.join(str(token) for token in tokens), limit=limit)

        # Append ORDER BY
        if order_by_index is not None:
            tokens = statements[0].tokens[order_by_index:]
            limited_query += '\n' + ''.join(str(token) for token in tokens)

        return limited_query
    

    def _limit_parsed_query(self, query: str, limit: int) -> str:
        raise NotImplementedError()
    

    def get_select_table_query(self, table: str|tuple, schema_only = False) -> T_Composed:
        """
        Build a query on the given table.

        If `schema_only` is given, no row will be returned (this is used to get information on the table).
        Otherwise, all rows will be returned.

        The return type of this function depends on the database engine.
        It is passed directly to the cursor's execute function for this engine.
        """
        raise NotImplementedError()


    def get_composable_param(self, value) -> T_Composable:
        if value is None:
            return "null"
        elif value == '__now__':
            return "CURRENT_DATETIME()"
        else:
            return self.escape_literal(value)
                

    def escape_identifier(self, value) -> T_Composable:
        raise NotImplementedError()
                

    def escape_literal(self, value) -> T_Composable:
        raise NotImplementedError()
    

    # -------------------------------------------------------------------------
    # Tables and columns
    #    

    @classmethod
    def split_name(cls, name: str|tuple) -> tuple[str,str]:
        if isinstance(name, tuple):
            return name
        
        try:
            pos = name.index('.')
            schema = name[0:pos]
            name = name[pos+1:]
        except ValueError:
            schema = cls.DEFAULT_SCHEMA
            name = name

        return (schema, name)
    

    def schema_exists(self, schema: str) -> bool:
        raise NotImplementedError()
    

    def create_schema(self, schema: str):
        raise NotImplementedError()
    

    def drop_schema(self, schema: str, cascade: bool = False):
        raise NotImplementedError()
    

    def table_exists(self, table: str|tuple) -> bool:
        raise NotImplementedError()


    def get_cursor_column_names(self, cursor: T_Cursor) -> list[str]:
        return [info[0] for info in cursor.description]
        

    def get_table_column_names(self, table: str|tuple) -> list[str]:
        query = self.get_select_table_query(table, schema_only=True)
        with self.execute_get_cursor(query) as cursor:
            return self.get_cursor_column_names(cursor)
    

    def drop_table(self, table: str|tuple):
        raise NotImplementedError()


    def truncate_table(self, table: str|tuple):
        raise NotImplementedError()


    def copy_from_csv(self, file: Path|str|IOBase, table: str|tuple, columns: list[str] = None, delimiter: str = None, quotechar: str = '"', nullchar: str = '', noheader: bool = False):
        raise NotImplementedError()
   

    # -------------------------------------------------------------------------
    # region Reinit (Django command)
    #    

    def move_all_to_new_schema(self, new_schema: str, old_schema: str = "public"):
        raise NotImplementedError()
    

    def drop_all(self, schema: str = "public"):
        raise NotImplementedError()
    
    # endregion


    def deploy_choices_table(self):
        raise NotImplementedError()


def _get_connection_from_wrapper(origin):    
    if type(origin).__module__.startswith(('django.db.backends.', 'django.utils.connection')):
        return origin.connection
    elif type(origin).__module__.startswith(('psycopg_pool.pool',)):
        return origin.connection()
    elif type(origin).__module__.startswith(('psycopg2.pool',)):
        return origin.getconn()
    else:
        return origin
