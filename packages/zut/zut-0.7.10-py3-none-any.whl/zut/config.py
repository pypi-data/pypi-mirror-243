from __future__ import annotations
import os
import re

import sys
from configparser import ConfigParser, _UNSET, NoOptionError, NoSectionError
from pathlib import Path

from .text import skip_bom


def get_config(prog: str) -> ExtendedConfigParser:
    """
    A function to search for configuration files in some common paths.
    """
    if not prog:
        raise ValueError("prog required")
        # NOTE: we should not try to determine prog here: this is too dangerous (invalid/fake configuration files could be loaded by mistake)

    parser = ExtendedConfigParser()

    parser.read([
        # System configuration
        Path(f'C:/ProgramData/{prog}.conf' if sys.platform == 'win32' else f'/etc/{prog}.conf').expanduser(),
        # User configuration
        Path(f'~/.config/{prog}.conf').expanduser(),
        # Local configuration
        "local.conf",
    ], encoding='utf-8')

    return parser


class ExtendedConfigParser(ConfigParser):
    def getsecret(self, section: str, option: str, *, raw=False, vars=None, fallback: str = _UNSET) -> str:
        """
        If option not found, will also try to read the value from:
        - A file named `/run/secrets/{section}_{option}` if exists (usefull for Docker secrets).
        - The file indicated by option `{option}_file` (usefull for password files).
        """
        result = self.get(section, option, raw=raw, vars=vars, fallback=None)

        if result is not None:
            return result

        # try secret
        secret_name = f'{section}_{option}'.replace(':', '-')
        secret_path = f'/run/secrets/{secret_name}'
        if os.path.exists(secret_path):
            return _read_file_and_rstrip_newline(secret_path)

        # try file
        path = self.get(section, f'{option}_file', raw=raw, vars=vars, fallback=None)
        if path is not None:
            return _read_file_and_rstrip_newline(path)
        
        if fallback is _UNSET:
            raise NoOptionError(option, section)
        else:
            return fallback


    def getlist(self, section: str, option: str, *, raw=False, vars=None, delimiter=',', fallback: list[str] = _UNSET) -> list[str]:
        values_str = self.get(section, option, raw=raw, vars=vars, fallback=fallback)
        if not isinstance(values_str, str):
            return values_str # fallback
        
        values = []
        for value in values_str.split(delimiter):
            value = value.strip()
            if not value:
                continue
            values.append(value)

        return values


def _read_file_and_rstrip_newline(path: os.PathLike):
    with open(path, 'r', encoding='utf-8') as fp:
        skip_bom(fp)
        value = fp.read()
        return value.rstrip('\r\n')
