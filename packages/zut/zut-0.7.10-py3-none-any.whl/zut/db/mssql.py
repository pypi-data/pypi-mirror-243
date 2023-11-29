from __future__ import annotations
import re
import logging
from urllib.parse import urlparse, unquote

from zut.text import build_url
from .base import DbAdapter

logger = logging.getLogger(__name__)

try:
    from pyodbc import Connection, Cursor, connect, drivers
except ImportError:
    Connection = type(None)
    Cursor = type(None)


class MssqlAdapter(DbAdapter[Connection, Cursor, str, str]):
    URL_SCHEME = 'mssql'
    DEFAULT_SCHEMA = 'dbo'
    ONLY_POSITIONAL_PARAMS = True
    EXPECTED_CONNECTION_TYPES = ['pyodbc.Connection']

    @classmethod
    def is_available(cls):
        return Connection != type(None)
    

    def _create_connection(self) -> Connection:
        r = urlparse(self._connection_url)
        
        server = unquote(r.hostname) or '(local)'
        if r.port:
            server += f',{r.port}'

        # Use "ODBC Driver XX for SQL Server" if available ("SQL Server" seems not to work with LocalDB, and takes several seconds to establish connection on my standard Windows machine with SQL Server Developer).
        driver = "SQL Server"
        for a_driver in drivers():
            if re.match(r'^ODBC Driver \d+ for SQL Server$', a_driver):
                driver = a_driver
                break

        connection_string = 'Driver={%s};Server=%s;Database=%s;' % (driver, server, r.path.lstrip('/'))

        def escape(s):
            if ';' in s or '{' in s or '}' in s or '=' in s:
                return "{" + s.replace('}', '}}') + "}"
            else:
                return s

        if r.username:
            connection_string += 'UID=%s;' % escape(unquote(r.username))
            if r.password:
                connection_string += 'PWD=%s;' % escape(unquote(r.password))
        else:
            connection_string += 'Trusted_Connection=yes;'

        return connect(connection_string, autocommit=self._autocommit)


    def _get_url_from_connection(self):
        with self.cursor() as cursor:
            cursor.execute("SELECT @@SERVERNAME, local_tcp_port, SUSER_NAME(), DB_NAME() FROM sys.dm_exec_connections WHERE session_id = @@spid")
            host, port, user, dbname = next(iter(cursor))
        return build_url(scheme=self.URL_SCHEME, username=user, hostname=host, port=port, path='/'+dbname)
    

    # -------------------------------------------------------------------------
    # Queries
    #
        
    def _limit_parsed_query(self, query: str, limit: int) -> str:
        return f"SELECT TOP {limit} * FROM ({query}) s"


    def get_select_table_query(self, table: str|tuple, schema_only = False) -> str:
        schema, table = self.split_name(table)
        
        query = f'SELECT * FROM {self.escape_identifier(schema)}.{self.escape_identifier(table)}'
        if schema_only:
            query += ' WHERE 1 = 0'

        return query
        

    def escape_identifier(self, value: str) -> str:
        return f"[{value.replace(']', ']]')}]"
    

    def escape_literal(self, value: str) -> str:
        return f"'" + value.replace("'", "''") + "'"
    

    # -------------------------------------------------------------------------
    # Tables and columns
    #    

    def table_exists(self, table: str|tuple) -> bool:        
        schema, table = self.split_name(table)

        query = "SELECT CASE WHEN EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = ? AND table_name = ?) THEN 1 ELSE 0 END"
        params = [schema, table]

        return self.execute_get_scalar(query, params)

        
    def truncate_table(self, table: str|tuple):
        schema, table = self.split_name(table)
        query = "TRUNCATE TABLE %s.%s" % (schema, table)
        self.execute(query)
