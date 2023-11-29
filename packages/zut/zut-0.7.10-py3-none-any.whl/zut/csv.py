from __future__ import annotations
import csv
import locale
from io import IOBase
from pathlib import Path
from typing import Any

from .text import skip_bom
from . import filesh


def get_csv_headers(csv_file: str|Path|IOBase, encoding: str = 'utf-8', delimiter: str = None, quotechar: str = '"') -> list[str]:        
    fp = None
    fp_to_close = None

    if delimiter is None:
        delimiter = get_default_csv_delimiter()

    try:        
        if isinstance(csv_file, (str,Path)):
            fp = filesh.open_file(csv_file, 'r', newline='', encoding=encoding)
            fp_to_close = fp
            if encoding == 'utf-8':
                skip_bom(fp)
        else:
            fp = csv_file
            fp.seek(0)
            
        reader = csv.reader(fp, delimiter=delimiter, quotechar=quotechar)
        try:
            return next(reader)
        except StopIteration:
            return None

    finally:
        if fp_to_close:
            fp_to_close.close()
        elif fp:
            fp.seek(0)


def get_csv_dict_list(csv_file: str|Path|IOBase, encoding: str = 'utf-8', delimiter: str = None, quotechar: str = '"') -> list[dict[str,Any]]:        
    fp = None
    fp_to_close = None

    if delimiter is None:
        delimiter = get_default_csv_delimiter()

    try:        
        if isinstance(csv_file, (str,Path)):
            fp = filesh.open_file(csv_file, 'r', newline='', encoding=encoding)
            fp_to_close = fp
            if encoding == 'utf-8':
                skip_bom(fp)
        else:
            fp = csv_file
            fp.seek(0)
            
        reader = csv.reader(fp, delimiter=delimiter, quotechar=quotechar)
        headers: list[str] = None
        data_list: list[dict[str,Any]] = []

        for row in reader:
            if headers is None:
                headers = row
                continue
            data = {headers[i]: value for i, value in enumerate(row)}
            data_list.append(data)

        return data_list

    finally:
        if fp_to_close:
            fp_to_close.close()
        elif fp:
            fp.seek(0)


def get_default_csv_delimiter():
    if locale.localeconv()['decimal_point'] == ',':
        return ';'
    else:
        return ','
