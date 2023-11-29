from functools import lru_cache
from .log_support import logger
from typing import Collection, Tuple
from .constant import CACHE_SIZE, UNKNOW

_ENGINE = None


class Engine:
    def __init__(self, name, trans_placeholder, show_sql = False):
        self.name = name
        self.show_sql = show_sql
        self.trans_placeholder = trans_placeholder

    @classmethod
    def init(cls, name=UNKNOW, trans_placeholder=None):
        cls.do_init(name, trans_placeholder, show_sql=False)

    @classmethod
    def do_init(cls, name, trans_placeholder, show_sql):
        global _ENGINE
        if _ENGINE:
            _ENGINE.show_sql = show_sql
            if _ENGINE.name is None or _ENGINE.name == UNKNOW:
                _ENGINE.name = name
            if _ENGINE.trans_placeholder is None:
                _ENGINE.trans_placeholder = trans_placeholder
        else:
            _ENGINE = cls(name, trans_placeholder, show_sql)

    @staticmethod
    def current_engine():
        global _ENGINE
        if _ENGINE:
            return _ENGINE.name
        return None

    @classmethod
    @lru_cache(maxsize=CACHE_SIZE)
    def create_insert_sql_intf(cls, table: str, cols: Tuple[str]):
        return _ENGINE.create_insert_sql(table, cols)

    @staticmethod
    def get_page_sql_args_intf(sql: str, page_num: int, page_size: int, *args):
        return _ENGINE.get_page_sql_args(sql, page_num, page_size, *args)

    @staticmethod
    def get_select_key_intf(*args, **kwargs):
        return _ENGINE.get_select_key(*args, **kwargs)

    @staticmethod
    def get_table_columns_intf(table: str):
        return _ENGINE.get_table_columns(table)

    @staticmethod
    def before_execute_intf(function: str, sql: str, *args):
        return _ENGINE.before_execute(function, sql, *args)

    @staticmethod
    def create_insert_sql(table: str, cols: Collection[str]):
        columns, placeholders = zip(*[('{}'.format(col), '?') for col in cols])
        return 'INSERT INTO {}({}) VALUES({})'.format(table, ', '.join(columns), ','.join(placeholders))

    def before_execute(self, function: str, sql: str, *args):
        if self.show_sql:
            logger.info("Exec func 'sqlexec.%s' \n\tSQL: %s \n\tARGS: %s" % (function, sql, args))
        if '%' in sql and 'like' in sql.lower():
            sql = sql.replace('%', '%%').replace('%%%%', '%%')
        if self.trans_placeholder:
            sql = sql.replace('?', '%s')
        return sql
