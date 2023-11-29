from __future__ import annotations

import atexit
import logging
import logging.config
import os
import sys

from .colors import Colors


def configure_logging(*, prog: str = None, count: bool = True):
    """
    Logging configuration (suitable by default for console applications).
    """
    config = get_logging_dict_config(prog=prog, count=count)

    logging.config.dictConfig(config)
    

def get_logging_dict_config(*, prog: str = None, count: bool = False):
    """
    Logging configuration (suitable by default for Django applications).
    """
    console_level, console_levelnum = _get_level_from_env('LOG_LEVEL', 'INFO')
    log_file_level, log_file_levelnum = _get_level_from_env('LOG_FILE_LEVEL')

    log_file = os.environ.get('LOG_FILE', None)
    if log_file or log_file_level:
        if not log_file:
            log_file = _get_default_log_file()
        elif log_file.upper() in ['1', 'TRUE']:
            log_file = _get_default_log_file()
        elif log_file.upper() in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
            if not log_file_level:
                log_file_level = log_file.upper()
                log_file_levelnum = logging.getLevelName(log_file_level)
            log_file = _get_default_log_file()
        else:
            if not log_file_level:
                log_file_level = 'INFO'
                log_file_levelnum = logging.getLevelName(log_file_level)

    root_level = log_file_level if log_file_levelnum is not None and log_file_levelnum < console_levelnum else console_level

    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                '()': ColoredFormatter.__module__ + '.' + ColoredFormatter.__qualname__,
                'format': '%(levelcolor)s%(levelname)s%(reset)s %(gray)s[%(name)s]%(reset)s %(levelcolor)s%(message)s%(reset)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console',
                'level': console_level,
            },
        },
        'root': {
            'handlers': ['console'],
            'level': root_level,
        },
        'loggers': {
            'django': { 'level': os.environ.get('DJANGO_LOG_LEVEL', '').upper() or 'INFO', 'propagate': False },
            'smbprotocol': { 'level': 'WARNING' },
        },
    }

    if count:
        config['handlers']['count'] = {
            'class': CountHandler.__module__ + '.' + CountHandler.__qualname__,
            'level': 'WARNING',
        }

        config['root']['handlers'].append('count')

    if log_file:
        config['formatters']['file'] = {
            'format': '%(asctime)s %(levelname)s [%(name)s] %(message)s',
        }

        config['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': log_file,
            'mode': 'a',
            'level': log_file_level or root_level,
        }

        config['root']['handlers'].append('file')

    return config


def _get_default_log_file():
    path = sys.argv[0]
    if path.endswith('__main__.py'):
        path = path[:-len('__main__.py')]
    if path.endswith(('/', '\\')):
        path = path[:-1]

    prog = os.path.basename(path)
    if prog.endswith('.py'):
        prog = prog[:-len('.py')]

    return f"{prog}.log"


def _get_level_from_env(varname: str = None, default: str = None) -> tuple[str,int|None]:
    level = os.environ.get(varname, '').upper() or default
    if not level:
        return ('', None)

    levelnum = logging.getLevelName(level)
    
    if not isinstance(levelnum, int):
        print(f"warning: invalid {varname} \"{level}\": fall back to \"{default or 'INFO'}\"")
        level = default or 'INFO'
        levelnum = logging.getLevelName(level)

    return (level, levelnum)


class ColoredRecord:
    LEVELCOLORS = {
        logging.DEBUG:     Colors.GRAY,
        logging.INFO:      '',
        logging.WARNING:   Colors.YELLOW,
        logging.ERROR:     Colors.RED,
        logging.CRITICAL:  Colors.BOLD_RED,
    }

    def __init__(self, record: logging.LogRecord):
        # The internal dict is used by Python logging library when formatting the message.
        # (inspired from library "colorlog").
        self.__dict__.update(record.__dict__)
        self.__dict__.update({
            'levelcolor': self.LEVELCOLORS.get(record.levelno, ''),
            'red': Colors.RED,
            'green': Colors.GREEN,
            'yellow': Colors.YELLOW,
            'cyan': Colors.CYAN,
            'gray': Colors.GRAY,
            'bold_red': Colors.BOLD_RED,
            'reset': Colors.RESET,
        })


class ColoredFormatter(logging.Formatter):
    def formatMessage(self, record: logging.LogRecord) -> str:
        """Format a message from a record object."""
        wrapper = ColoredRecord(record)
        message = super().formatMessage(wrapper)
        return message


class CountHandler(logging.Handler):
    def __init__(self, level=logging.WARNING):
        self.counts: dict[int, int] = {}
        atexit.register(self.print_counts)
        super().__init__(level=level)

    def print_counts(self):
        msg = ""

        levelnos = sorted(self.counts.keys(), reverse=True)
        for levelno in levelnos:
            levelname = logging.getLevelName(levelno)
            levelcolor = ColoredRecord.LEVELCOLORS.get(levelno, '')
            msg += (", " if msg else "") + f"{levelcolor}%s{Colors.RESET}" % levelname + ": %d" % self.counts[levelno]

        if msg:
            print("Logged " + msg, file=sys.stderr)

    def emit(self, record: logging.LogRecord):
        if record.levelno >= self.level:
            if not record.levelno in self.counts:
                self.counts[record.levelno] = 1
            else:
                self.counts[record.levelno] += 1
