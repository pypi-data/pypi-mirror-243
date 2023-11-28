import functools
from . import sql_support
from .engine import Engine
from typing import Collection
from .csv_support import CsvWriter
from .init_import import import_driver, get_engine
from .log_support import logger, insert_log, save_log, do_sql_log, sql_log
from .support import DBCtx, ConnectionCtx, Dict, MultiColumnsError, TransactionCtx, try_commit, DBError, DB_LOCK
from .constant import MYSQL_CONNECTOR_DRIVER, SQLITE, PARAM_DRIVER, PARAM_SHOW_SQL, PARAM_TRANS_PLACEHOLDER, PARAM_DEBUG, PARAM_POOL_SIZE

_DB_CTX = None
_POOLED = False


def init_db(*args, **kwargs):
    """
    Compliant with the Python DB API 2.0 (PEP-249).

    from sqlexec
    sqlexec.init_db('test.db', driver='sqlite3', show_sql=True, debug=True)
    or
    sqlexec.init_db("postgres://user:password@127.0.0.1:5432/testdb", driver='psycopg2', pool_size=5, show_sql=True, debug=True)
    or
    sqlexec.init_db(user='root', password='xxx', host='127.0.0.1', port=3306, database='testdb', driver='pymysql', pool_size=5, show_sql=True, debug=True)

    Addition parameters:
    :param driver=None: str, import driver, 'import pymysql'
    :param pool_size=0: int, default 0, size of connection pool
    :param show_sql=False: bool,  if True, print sql
    :param debug=False: bool, if True, print debug context
    :param trans_placeholder=True: bool, if True, sql placeholder '?' --> '%s'

    Other parameters of connection pool refer to DBUtils: https://webwareforpython.github.io/DBUtils/main.html#pooleddb-pooled-db
    """

    global _DB_CTX
    pool_size = 0
    driver = kwargs.pop(PARAM_DRIVER) if PARAM_DRIVER in kwargs else None
    show_sql = kwargs.pop(PARAM_SHOW_SQL) if PARAM_SHOW_SQL in kwargs else False
    trans_placeholder = kwargs.pop(PARAM_TRANS_PLACEHOLDER) if PARAM_TRANS_PLACEHOLDER in kwargs else True

    curr_engine = get_engine(driver, *args, **kwargs)
    engine, driver, creator = import_driver(driver, curr_engine)
    prepared = MYSQL_CONNECTOR_DRIVER == driver
    if PARAM_DEBUG in kwargs and kwargs.pop(PARAM_DEBUG):
        from logging import DEBUG
        logger.setLevel(DEBUG)

    if PARAM_POOL_SIZE in kwargs:
        # mysql.connector 用自带连接池
        pool_size = kwargs[PARAM_POOL_SIZE] if prepared else kwargs.pop(PARAM_POOL_SIZE)

    pool_args = ['mincached', 'maxcached', 'maxshared', 'maxconnections', 'blocking', 'maxusage', 'setsession', 'reset', 'failures', 'ping']
    pool_kwargs = {key: kwargs.pop(key) for key in pool_args if key in kwargs}
    connect = lambda: creator.connect(*args, **kwargs)
    if pool_size >= 1 and not prepared:
        from .pooling import pooled_connect
        global _POOLED
        _POOLED = True
        connect = pooled_connect(connect, pool_size, **pool_kwargs)

    with DB_LOCK:
        if _DB_CTX is not None:
            raise DBError('DB is already initialized.')
        _DB_CTX = DBCtx(connect=connect, prepared=prepared)

    if SQLITE == engine:
        trans_placeholder = False
    Engine.do_init(engine, trans_placeholder, show_sql)
    if pool_size > 0:
        logger.info("Inited db engine <%s> of %s with driver: '%s' and pool size: %d." % (hex(id(_DB_CTX)), engine, driver, pool_size))
    else:
        logger.info("Inited db engine <%s> of %s with driver: '%s'." % (hex(id(_DB_CTX)), engine, driver))


def connection():
    """
    Return ConnectionCtx object that can be used by 'with' statement:

    with connection():
        pass
    """
    global _DB_CTX
    return ConnectionCtx(_DB_CTX)


def with_connection(func):
    """
    Decorator for reuse connection.

    @with_connection
    def foo(*args, **kw):
        f1()
        f2()
    """

    global _DB_CTX
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with ConnectionCtx(_DB_CTX):
            return func(*args, **kw)
    return _wrapper


def transaction():
    """
    Create a transaction object so can use with statement:

    with transaction():
        pass
    with transaction():
         insert(...)
         update(... )
    """
    global _DB_CTX
    return TransactionCtx(_DB_CTX)


def with_transaction(func):
    """
    A decorator that makes function around transaction.

    @with_transaction
    def update_profile(id, name, rollback):
         u = dict(id=id, name=name, email='%s@test.org' % name, passwd=name, last_modified=time.time())
         insert('person', **u)
         r = update('update person set passwd=? where id=?', name.upper(), id)
    """
    global _DB_CTX
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with TransactionCtx(_DB_CTX):
            return func(*args, **kw)
    return _wrapper


def execute(sql: str, *args, **kwargs):
    """
    Execute sql return effect rowcount

    sql: INSERT INTO person(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
         INSERT INTO person(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = try_mapping('sqlexec.execute', sql, *args, **kwargs)
    return do_execute(sql, *args)


def insert(table: str, **kwargs):
    """
    Insert data into table, return effect rowcount.

    :param table: table name
    :param kwargs: {name='张三', age=20}
    return: Effect rowcount
    """
    insert_log('insert', table, **kwargs)
    sql, args = sql_support.insert_sql_args(table.strip(), **kwargs)
    return execute(sql, *args)


def save(select_key: str, table: str, **kwargs) -> int:
    """
    Insert data into table, return primary key.

    :param select_key: sql for select primary key
    :param table: table
    :param kwargs: {name='张三', age=20}
    :return: Primary key
    """
    save_log('save', select_key, table, **kwargs)
    sql, args = sql_support.insert_sql_args(table.strip(), **kwargs)
    return save_sql(select_key, sql, *args)


def save_sql(select_key: str, sql: str, *args, **kwargs):
    """
    Insert data into table, return primary key.

    sql: INSERT INTO person(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
         INSERT INTO person(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}

    :param select_key: sql for select primary key
    :return: Primary key
    """
    logger.debug("Exec func 'sqlexec.%s', 'select_key': %s \n\t sql: %s \n\t args: %s \n\t kwargs: %s" % ('save_sql', select_key, sql, args, kwargs))
    sql, args = sql_support.get_mapping_sql_args(sql, *args, **kwargs)
    return do_save_sql(select_key, sql, *args)


def get(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one int and only one int result, SQL contain 'limit'.

    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT count(1) FROM person WHERE name=:name and age=:age limit 1  --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = try_mapping('sqlexec.get', sql, *args, **kwargs)
    return do_get(sql, *args)


def select(sql: str, *args, **kwargs):
    """
    execute select SQL and return unique result or list results(tuple).

    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = try_mapping('sqlexec.select', sql, *args, **kwargs)
    return do_select(sql, *args)


def select_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and return unique result(tuple), SQL contain 'limit'.

    sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age limit 1 --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = try_mapping('sqlexec.select_one', sql, *args, **kwargs)
    return do_select_one(sql, *args)


def query(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = try_mapping('sqlexec.query', sql, *args, **kwargs)
    return do_query(sql, *args)


def query_one(sql: str, *args, **kwargs):
    """
    execute select SQL and return unique result(dict), SQL contain 'limit'.

    sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age limit 1 --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = try_mapping('sqlexec.query_one', sql, *args, **kwargs)
    return do_query_one(sql, *args)


def do_execute(sql: str, *args):
    """
    Execute sql return effect rowcount

    sql: insert into person(name, age) values(?, ?)  -->  args: ('张三', 20)
    """
    return _execute(None, sql, *args)


def do_save_sql(select_key: str, sql: str, *args):
    """
    Insert data into table, return primary key.

    :param select_key: sql for select primary key
    :param sql: SQL
    :param args:
    :return: Primary key
    """
    return _execute(select_key, sql, *args)


def do_get(sql: str, *args):
    """
    Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
    MultiColumnsError: Expect only one column.

    sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    do_sql_log('sqlexec.do_get', sql, *args)
    result, _ = _select_one(sql, *args)
    if result:
        if len(result) == 1:
            return result[0]
        msg = "Exec func 'sqlexec.%s' expect only one column but %d." % ('do_get', len(result))
        logger.error('%s  \n\t sql: %s \n\t args: %s' % (msg, sql, args))
        raise MultiColumnsError(msg)
    return None


def do_select(sql: str, *args):
    """
    execute select SQL and return unique result or list results(tuple).
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    results, _ = _select(sql, *args)
    return results


def do_select_one(sql: str, *args):
    """
    Execute select SQL and return unique result(tuple), SQL contain 'limit'.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    result, _ = _select_one(sql, *args)
    return result


def do_query(sql: str, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    results, description = _select(sql, *args)
    if results and description:
        names = list(map(lambda x: x[0], description))
        return list(map(lambda x: Dict(names, x), results))
    return results


def do_query_one(sql: str, *args):
    """
    execute select SQL and return unique result(dict), SQL contain 'limit'.
    sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
    """
    result, description = _select_one(sql, *args)
    if result and description:
        names = list(map(lambda x: x[0], description))
        return Dict(names, result)
    return result


def batch_insert(table: str, *args):
    """
    Batch insert
    :param table: table name
    :param args: All number must have same key. [{'name': '张三', 'age': 20}, {'name': '李四', 'age': 28}]
    :return: Effect row count
    """
    logger.debug("Exec func 'sqlexec.%s' \n\t Table: '%s', args: %s" % ('batch_insert', table, args))
    sql, args = sql_support.batch_insert_sql_args(table, *args)
    return batch_execute(sql, *args)


@with_connection
def batch_execute(sql: str, *args):
    """
    Batch execute sql return effect rowcount
    :param sql: insert into person(name, age) values(?, ?)  -->  args: [('张三', 20), ('李四', 28)]
    :param args: All number must have same size.
    :return: Effect rowcount
    """
    global _DB_CTX
    cursor = None
    assert args, "*args must not be empty."
    if isinstance(args[0], dict):
        sql, args = sql_support.batch_named_sql_args(sql, *args)
    sql = Engine.before_execute_intf('batch_execute', sql.strip(), *args)
    args = sql_support.get_batch_args(*args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.executemany(sql, args)
        effect_rowcount = cursor.rowcount
        try_commit(_DB_CTX)
        return effect_rowcount
    finally:
        if cursor:
            cursor.close()


def csv(sql: str, *args, **kwargs) -> CsvWriter:
    """
    Execute select SQL and save a csv

    sqlexec.csv('select id, name, age from person WHERE name=:name', name='张三').save('test.csv', delimiter=',', header=True)

    :param sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
                SELECT * FROM person WHERE name=:name and age=:age limit 1 --> kwargs: {'name': '张三', 'age': 20}
    :return: CsvWriter
    """
    sql, args = try_mapping('sqlexec.csv', sql, *args, **kwargs)
    return to_csv(sql, *args)


def to_csv(sql: str, *args) -> CsvWriter:
    """
    Execute select SQL and save a csv

    sqlexec.to_csv('select id, name, age from person WHERE name = ?', '张三').save('test.csv', delimiter=',', header=True)

    :param sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
    :return: CsvWriter
    """
    result, description = _select(sql, *args)
    return CsvWriter(result, description)


def df(sql: str, *args, **kwargs):
    """
    Execute select SQL and return DataFrame of pandas.

    sqlexec.df('select id, name, age from person WHERE name=:name', name='张三')

    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM person WHERE name=:name and age=:age --> kwargs: {'name': '张三', 'age': 20}

    :return DataFrame of pandas
    """
    sql, args = try_mapping('sqlexec.csv', sql, *args, **kwargs)
    return to_df(sql, *args)


def to_df(sql: str, *args):
    """
    Execute select SQL and return DataFrame of pandas.

    sqlexec.to_df('select id, name, age from person WHERE name = ?', '张三')

    sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)

    :return DataFrame of pandas
    """
    import pandas as pd
    result, description = _select(sql, *args)
    description = list(map(lambda x: x[0], description))
    return pd.DataFrame(data=result, columns=description)


def insert_from_csv(file_name: str, table: str, delimiter=',', header=True, columns: Collection[str] = None):
    """
    sqlexec.insert_from_csv('test.csv', 'user')
    """
    import csv
    sql = None
    if columns and len(columns) > 0:
        sql = sql_support.insert_sql(table.strip(), columns)
    elif not header:
        raise ValueError("'header' and 'columns' must have one.")

    with open(file_name, newline='', encoding='utf-8') as f:
        lines = csv.reader(f, delimiter=delimiter)
        lines = [line for line in lines]

        if header:
            if sql is None:
                sql = sql_support.insert_sql(table.strip(), lines[0])
            lines = lines[1:]

    return batch_execute(sql, lines)


def insert_from_df(df, table: str, columns: Collection[str] = None):
    """
    sqlexec.insert_from_df(df, 'user')
    """
    columns = columns if columns and len(columns) > 0 else df.columns.tolist()
    sql = sql_support.insert_sql(table.strip(), columns)
    return batch_execute(sql, df.values.tolist())


def get_connection():
    global _DB_CTX
    _DB_CTX.try_init()
    return _DB_CTX.connection


def close():
    global _POOLED
    if _POOLED:
        from .pooling import close_pool
        close_pool()


@with_connection
def _execute(select_key: str, sql: str, *args):
    global _DB_CTX
    cursor = None
    logger.debug("Exec func 'sqlexec.%s', 'select_key': %s" % ('_execute', select_key))
    sql = Engine.before_execute_intf('_execute', sql, *args)
    try:
        cursor = _DB_CTX.connection.cursor()
        cursor.execute(sql, args)
        if select_key:
            cursor.execute(select_key)
            result = cursor.fetchone()[0]
        else:
            result = cursor.rowcount
        try_commit(_DB_CTX)
        return result
    finally:
        if cursor:
            cursor.close()


@with_connection
def _select(sql: str, *args):
    global _DB_CTX
    cursor = None
    sql = Engine.before_execute_intf('do_select', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        return cursor.fetchall(), cursor.description
    finally:
        if cursor:
            cursor.close()


@with_connection
def _select_one(sql: str, *args):
    global _DB_CTX
    cursor = None
    sql, args = _do_limit_sql_args('sqlexec._select_one', sql, *args)
    sql = Engine.before_execute_intf('_select_one', sql.strip(), *args)
    try:
        cursor = _DB_CTX.cursor()
        cursor.execute(sql, args)
        return cursor.fetchone(), cursor.description
    finally:
        if cursor:
            cursor.close()


def try_mapping(function, sql, *args, **kwargs):
    sql_log(function, sql, *args, **kwargs)
    return sql_support.get_mapping_sql_args(sql, *args, **kwargs)


def _do_limit_sql_args(function, sql, *args):
    do_sql_log(function, sql, *args)
    return sql_support.limit_one_sql_args(sql, *args)
