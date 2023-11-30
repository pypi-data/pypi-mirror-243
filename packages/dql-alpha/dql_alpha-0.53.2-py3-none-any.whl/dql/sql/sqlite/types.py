import json
import sqlite3

from sqlalchemy import types

from dql.sql.types import TypeConverter

try:
    import numpy as np

    numpy_imported = True
except ImportError:
    numpy_imported = False


class Array(types.UserDefinedType):
    cache_ok = True

    def __init__(self, item_type):  # pylint: disable=super-init-not-called
        self.item_type = item_type

    @property
    def python_type(self):
        return list

    def get_col_spec(self, **kwargs):  # pylint: disable=unused-argument
        return "ARRAY"


def adapt_array(arr):
    return json.dumps(arr)


def convert_array(arr):
    return json.loads(arr)


def adapt_np_array(arr):
    return json.dumps(arr.tolist())


def adapt_np_generic(val):
    return val.tolist()


def register_type_converters():
    sqlite3.register_adapter(list, adapt_array)
    sqlite3.register_converter("ARRAY", convert_array)
    if numpy_imported:
        sqlite3.register_adapter(np.ndarray, adapt_np_array)
        sqlite3.register_adapter(np.int32, adapt_np_generic)
        sqlite3.register_adapter(np.int64, adapt_np_generic)
        sqlite3.register_adapter(np.float32, adapt_np_generic)
        sqlite3.register_adapter(np.float64, adapt_np_generic)


class SQLiteTypeConverter(TypeConverter):
    def array(self, item_type):
        return Array(item_type)
