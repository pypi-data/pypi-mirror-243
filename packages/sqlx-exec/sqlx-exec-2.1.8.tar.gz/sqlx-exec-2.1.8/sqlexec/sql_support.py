import re
from .engine import Engine
from .support import DBError
from typing import Collection
from functools import lru_cache
from .constant import CACHE_SIZE, NAMED_REGEX, LIMIT_1


def insert_sql(table: str, cols: Collection[str]):
    cols = cols if isinstance(cols, tuple) else tuple(cols)
    return Engine.create_insert_sql_intf(table, cols)

def insert_sql_args(table: str, **kwargs):
    cols, args = zip(*kwargs.items())
    sql = Engine.create_insert_sql_intf(table, cols)
    return sql, args


def get_batch_args(*args):
    return args[0] if isinstance(args, tuple) and len(args) == 1 and isinstance(args[0], Collection) else args


def batch_insert_sql_args(table: str, *args):
    args = get_batch_args(*args)
    args = [zip(*arg.items()) for arg in args]  # [(cols, args)]
    cols, args = zip(*args)  # (cols), (args)
    sql = Engine.create_insert_sql_intf(table, cols[0])
    return sql, args


def batch_named_sql_args(sql: str, *args):
    args = get_batch_args(*args)
    args = [get_named_args(sql, **arg) for arg in args]
    sql = get_named_sql(sql)
    return sql, args


@lru_cache(maxsize=CACHE_SIZE)
def get_named_sql(sql: str):
    return re.sub(NAMED_REGEX, '?', sql)


def get_named_args(sql: str, **kwargs):
    return [kwargs[r[1:]] for r in re.findall(NAMED_REGEX, sql)]


def get_named_sql_args(sql: str, **kwargs):
    args = get_named_args(sql, **kwargs)
    return get_named_sql(sql), args


def limit_one_sql_args(sql: str, *args):
    if require_limit(sql):
        return '{} LIMIT ?'.format(sql), [*args, LIMIT_1]
    return sql, args


def require_limit(sql: str):
    lower_sql = sql.lower()
    if 'limit' not in lower_sql:
        return True
    idx = lower_sql.rindex('limit')
    if idx > 0 and ')' in lower_sql[idx:]:
        return True
    return False


def is_mapping(sql: str):
    return ':' in sql


def is_placeholder(sql: str):
    return '?' in sql


def get_mapping_sql_args(sql: str, *args, **kwargs):
    if is_mapping(sql):
        assert kwargs, "Named mapping SQL expect '**kwargs' should not be empty."
        return get_named_sql_args(sql, **kwargs)

    if is_placeholder(sql) and not args:
        raise DBError("Placeholder sql expect '*args' should not be empty.")

    return sql, args
