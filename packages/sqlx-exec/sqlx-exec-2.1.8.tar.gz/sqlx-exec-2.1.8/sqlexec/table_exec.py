#！/usr/bin/env python3
# -*- coding:utf-8 -*-

from . import exec
from .csv_support import CsvWriter
from .constant import LIMIT_1, SELECT_COUNT
from typing import Sequence, Union, List, Tuple


class WhereExec:

    def __init__(self, table, executor, **where_condition):
        self.table = table
        self.executor = executor
        self.where_condition = where_condition

    def get(self, column: str):
        """
        Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
        MultiColumnsError: Expect only one column.

        sqlexec.table('user').where(name='李四').get('id')
        """
        where, args, _ = get_where_arg_limit(**self.where_condition)
        sql = get_select_sql(self.table, where, LIMIT_1, column)
        return self.executor.do_get(sql, *args, LIMIT_1)

    def count(self):
        """
         sqlexec.table('user').where(name='李四').count()
        """
        return self.get(SELECT_COUNT)

    def select(self, *columns):
        """
        sqlexec.table('user').where(name='李四').select('name', 'age')
        """
        where, args, limit = get_where_arg_limit(**self.where_condition)
        sql = get_select_sql(self.table, where, limit, *columns)
        if limit:
            if isinstance(limit, int):
                args = [*args, limit]
            else:
                args = [*args, *limit]
        return self.executor.do_select(sql, *args)

    def select_one(self, *columns):
        """
        sqlexec.table('user').where(name='李四').select_one('name', 'age')
        """
        where, args, _ = get_where_arg_limit(**self.where_condition)
        sql = get_select_sql(self.table, where, LIMIT_1, *columns)
        return self.executor.do_select_one(sql, *args, LIMIT_1)

    def query(self, *columns):
        """
        sqlexec.table('user').where(name='李四').query('name', 'age')
        """
        where, args, limit = get_where_arg_limit(**self.where_condition)
        sql = get_select_sql(self.table, where, limit, *columns)
        if limit:
            if isinstance(limit, int):
                args = [*args, limit]
            else:
                args = [*args, *limit]
        return self.executor.do_query(sql, *args)

    def query_one(self, *columns):
        """
        sqlexec.table('user').where(name__eq='李四').query_one('name', 'age')
        """
        where, args, _ = get_where_arg_limit(**self.where_condition)
        sql = get_select_sql(self.table, where, LIMIT_1, *columns)
        return self.executor.do_query_one(sql, *args, LIMIT_1)

    def delete(self):
        """
        sqlexec.table('user').where(name='李四').delete()
        """
        where, args, _ = get_where_arg_limit(**self.where_condition)
        sql = 'DELETE FROM %s %s' % (self.table, where)
        return self.executor.do_execute(sql, *args)

    def update(self, **kwargs):
        """
        sqlexec.table('user').where(name='张三').update(name='李四', age=45)
        """
        where, args, _ = get_where_arg_limit(**self.where_condition)
        update_cols, update_args = zip(*kwargs.items())
        args = [*update_args, *args]
        update_cols = ', '.join(['{} = ?'.format(col) for col in update_cols])
        sql = 'UPDATE {} SET {} {}'.format(self.table, update_cols, where)
        return self.executor.do_execute(sql, *args)

    def csv(self, *columns) -> CsvWriter:
        """
        sqlexec.table('user').where(name='张三').csv('name', 'age').save('test.csv', delimiter='', header=False)
        """
        where, args, limit = get_where_arg_limit(**self.where_condition)
        sql = get_select_sql(self.table, where, limit, *columns)
        if limit:
            if isinstance(limit, int):
                args = [*args, limit]
            else:
                args = [*args, *limit]
        return self.executor.to_csv(sql, *args)

    def df(self, *columns):
        """
        sqlexec.table('user').where(name='张三').df('name', 'age')
        :return DataFrame of pandas
        """
        where, args, limit = get_where_arg_limit(**self.where_condition)
        sql = get_select_sql(self.table, where, limit, *columns)
        if limit:
            if isinstance(limit, int):
                args = [*args, limit]
            else:
                args = [*args, *limit]
        return self.executor.to_df(sql, *args)


class TableExec:

    def __init__(self, table, executor):
        self.table = table
        self.executor = executor

    def insert(self, **kwargs):
        """
        Insert data into table, return effect rowcount.

        :param kwargs: {name='张三', age=20}
        return: Effect rowcount
        """
        return self.executor.insert(self.table, **kwargs)

    def save(self, select_key: str, **kwargs):
        """
        Insert data into table, return primary key.

        :param select_key: sql for select primary key
        :param kwargs:
        :return: Primary key
        """
        return self.executor.save(select_key, self.table, **kwargs)

    def get(self, column: str):
        """
        Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
        MultiColumnsError: Expect only one column.

        sqlexec.table('user').get('count(1)')
        """
        sql = get_select_sql(self.table, '', LIMIT_1, column)
        return self.executor.do_get(sql, LIMIT_1)

    def count(self):
        """
        sqlexec.table('user').count()
        """
        return self.get(SELECT_COUNT)

    def select(self, *columns):
        """
        sqlexec.table('user').select('name', 'age')
        """
        sql = get_select_sql(self.table, '', 0, *columns)
        return self.executor.do_select(sql)

    def select_one(self, *columns):
        """
        sqlexec.table('user').select_one('name', 'age')
        """
        sql = get_select_sql(self.table, '', LIMIT_1, *columns)
        return self.executor.do_select_one(sql, LIMIT_1)

    def query(self, *columns):
        """
        sqlexec.table('user').query('name', 'age')
        """
        sql = get_select_sql(self.table, '', 0, *columns)
        return self.executor.do_query(sql)

    def query_one(self, *columns):
        """
        sqlexec.table('user').query_one('name', 'age')
        """
        sql = get_select_sql(self.table, '', LIMIT_1, *columns)
        return self.executor.do_query_one(sql, LIMIT_1)

    def batch_insert(self, *args):
        """
        Execute sql return effect rowcount
        :param args: [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
        """
        return self.executor.batch_insert(self.table, *args)

    def csv(self, *columns) -> CsvWriter:
        """
        sqlexec.table('user').csv('name', 'age').save('test.csv', delimiter='', header=False)
        """
        sql = get_select_sql(self.table, '', 0, *columns)
        return self.executor.to_csv(sql)

    def df(self, *columns):
        """
        sqlexec.table('user').df('name', 'age')
        """
        sql = get_select_sql(self.table, '', 0, *columns)
        return self.executor.to_df(sql)

    def insert_from_csv(self, file_name: str, delimiter=',', header=True, columns: Tuple[str] = None):
        """
        sqlexec.table('user').insert_from_csv('test.csv')
        """
        return self.executor.insert_from_csv(file_name, self.table, delimiter, header, columns)

    def insert_from_df(self, df, columns: Tuple[str] = None):
        """
        sqlexec.table('user').insert_from_df(df)
        """
        return self.executor.insert_from_df(df, self.table, columns)

    def where(self, **kwargs) -> WhereExec:
        return WhereExec(self.table, self.executor, **kwargs)


def table(table: str) -> TableExec:
    table = table.strip()
    assert table, "Parameter 'table' must not be none"
    return TableExec(table, exec)


def get_select_sql(table: str, where: str, limit: Union[int, Tuple[int], List[int]], *columns):
    columns = ','.join([col if '(' in col else '{}'.format(col) for col in columns]) if columns else '*'

    if limit:
        if isinstance(limit, int):
            return 'SELECT {} FROM {} {} LIMIT ?'.format(columns, table, where)
        elif (isinstance(limit, Tuple) or isinstance(limit, List)) and len(limit) == 2:
            return 'SELECT {} FROM {} {} LIMIT ? OFFSET ?'.format(columns, table, where)
        else:
            raise ValueError("The type of the parameter 'limit' must be 'int' or tuple, list, and it length is 2.")
    else:
        return 'SELECT {} FROM {} {}'.format(columns, table, where)


def get_condition_arg(k: str, v: object):
    if k.endswith("__eq"):
        return "{} = ?".format(k[:-4]), v
    if k.endswith("__ne"):
        return "{} != ?".format(k[:-4]), v
    if k.endswith("__gt"):
        return "{} > ?".format(k[:-4]), v
    if k.endswith("__lt"):
        return "{} < ?".format(k[:-4]), v
    if k.endswith("__ge"):
        return "{} >= ?".format(k[:-4]), v
    if k.endswith("__gte"):
        return "{} >= ?".format(k[:-5]), v
    if k.endswith("__le"):
        return "{} <= ?".format(k[:-4]), v
    if k.endswith("__lte"):
        return "{} <= ?".format(k[:-5]), v
    if k.endswith("__isnull"):
        return "{} is {}".format(k[:-8], 'null' if v else 'not null'), None
    if k.endswith("__in") and isinstance(v, Sequence) and not isinstance(v, str):
        return "{} in({})".format(k[:-4], ','.join(['?' for _ in v])), v
    if k.endswith("__in"):
        return "{} in({})".format(k[:-4], '?'), v
    if k.endswith("__not_in") and isinstance(v, Sequence) and not isinstance(v, str):
        return "{} not in({})".format(k[:-8], ','.join(['?' for _ in v])), v
    if k.endswith("__not_in"):
        return "{} not in({})".format(k[:-8], '?'), v
    if k.endswith("__like"):
        return "{} like ?".format(k[:-6], '?'), v
    if k.endswith("__startswith"):
        return "{} like ?".format(k[:-12]), '{}%'.format(v)
    if k.endswith("__endswith"):
        return "{} like ?".format(k[:-10]), '%{}'.format(v)
    if k.endswith("__contains"):
        return "{} like ?".format(k[:-10]), '%{}%'.format(v)
    if k.endswith("__range") and isinstance(v, Sequence) and 2 == len(v) and not isinstance(v, str):
        col = k[:-7]
        return "{} >= ? and {} <= ?".format(col, col), v
    if k.endswith("__between") and isinstance(v, Sequence) and 2 == len(v) and not isinstance(v, str):
        return "{} between ? and ?".format(k[:-9]), v
    if k.endswith("__range") or k.endswith("__between"):
        return ValueError("Must is instance of Sequence with length 2 when use range or between statement")

    return "{} = ?".format(k), v


def get_where_arg_limit(**kwargs):
    where, args, limit = '', [], 0
    if 'limit' in kwargs:
        limit = kwargs.pop('limit')

    if kwargs:
        conditions, tmp_args = zip(*[get_condition_arg(k, v) for k, v in kwargs.items()])
        tmp_args = [arg for arg in tmp_args if arg is not None]

        for arg in tmp_args:
            if arg:
                if isinstance(arg, Sequence) and not isinstance(arg, str):
                    args.extend(arg)
                else:
                    args.append(arg)
        where = 'WHERE {}'.format(' and '.join(conditions))

    return where, args, limit