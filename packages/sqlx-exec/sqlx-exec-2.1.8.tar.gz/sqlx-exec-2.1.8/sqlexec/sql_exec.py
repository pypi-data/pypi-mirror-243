from . import exec
from .csv_support import CsvWriter


class SqlExec:

    def __init__(self, sql, executor):
        self.sql = sql
        self.executor = executor

    def execute(self, *args, **kwargs) -> int:
        """
        Execute sql return effect rowcount

        sql: INSERT INTO person(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
             INSERT INTO person(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.execute(self.sql, *args, **kwargs)

    def save(self, select_key: str, *args, **kwargs):
        """
        Insert data into table, return primary key.

        :param select_key: sql for select primary key
        :param args:
        :return: Primary key
        """
        return self.executor.save_sql(select_key, self.sql, *args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
        MultiColumnsError: Expect only one column.

        sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
             SELECT count(1) FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.get(self.sql, *args, **kwargs)

    def select(self, *args, **kwargs):
        """
        execute select SQL and return unique result or list results(tuple).

        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.select(self.sql, *args, **kwargs)

    def select_one(self, *args, **kwargs):
        """
        Execute select SQL and return unique result(tuple), SQL contain 'limit'.

        sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
             SELECT * FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.select_one(self.sql, *args, **kwargs)

    def query(self, *args, **kwargs):
        """
        Execute select SQL and return list results(dict).

        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.query(self.sql, *args, **kwargs)

    def query_one(self, *args, **kwargs):
        """
        execute select SQL and return unique result(dict), SQL contain 'limit'.

        sql: SELECT * FROM person WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
             SELECT * FROM person WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.query_one(self.sql, *args, **kwargs)

    def do_execute(self, *args):
        """
        Execute sql return effect rowcount

        sql: insert into person(name, age) values(?, ?)  -->  args: ('张三', 20)
        """
        return self.executor.do_execute(None, self.sql, *args)

    def do_save_sql(self, select_key: str, *args):
        """
        Insert data into table, return primary key.

        :param select_key: sql for select primary key
        :param args:
        :return: Primary key
        """
        return self.executor.do_save_sql(select_key, self.sql, *args)

    def do_get(self, *args):
        """
        Execute select SQL and expected one int and only one int result, SQL contain 'limit'.
        MultiColumnsError: Expect only one column.

        sql: SELECT count(1) FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
        """
        return self.executor.do_get(self.sql, *args)

    def do_select(self, *args):
        """
        execute select SQL and return unique result or list results(tuple).

        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.executor.do_select(self.sql, *args)

    def do_select_one(self, *args):
        """
        Execute select SQL and return unique result(tuple), SQL contain 'limit'.

        sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
        """
        return self.executor.do_select_one(self.sql, *args)

    def do_query(self, *args):
        """
        Execute select SQL and return list results(dict).

        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.executor.do_query(self.sql, *args)

    def do_query_one(self, *args):
        """
        execute select SQL and return unique result(dict), SQL contain 'limit'.

        sql: SELECT * FROM person WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
        """
        return self.executor.do_query_one(self.sql, *args)

    def batch_execute(self, *args):
        """
        Batch execute sql return effect rowcount

        sql: insert into person(name, age) values(?, ?)  -->  args: [('张三', 20), ('李四', 28)]

        :param args: All number must have same size.
        :return: Effect rowcount
        """
        return self.executor.batch_execute(self.sql, *args)

    def csv(self, *args, **kwargs) -> CsvWriter:
        """
        sqlexec.sql('select id, name, age from person WHERE name = :name').csv(name='张三').save('test.csv', delimiter=',', header=True)
        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM person WHERE name = :name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.csv(self.sql, *args, **kwargs)

    def to_csv(self, *args) -> CsvWriter:
        """
        sqlexec.sql('select id, name, age from person WHERE name = ?').to_csv('张三').save('test.csv', delimiter='', header=False)
        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.executor.to_csv(self.sql, *args)

    def df(self, *args, **kwargs):
        """
        sqlexec.sql('select id, name, age from person WHERE name = :name').df(name='张三')
        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM person WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        :return DataFrame of pandas
        """
        return self.executor.df(self.sql, *args, **kwargs)

    def to_df(self, *args):
        """
        sqlexec.sql('select id, name, age from person WHERE name = ?').to_df('张三').save('tt.csv', delimiter='', header=False)
        sql: SELECT * FROM person WHERE name=? and age=?  -->  args: ('张三', 20)
        :return DataFrame of pandas
        """
        return self.executor.to_df(self.sql, *args)


def sql(sql: str) -> SqlExec:
    sql = sql.strip()
    assert sql, "Parameter 'sql' must not be none"
    return SqlExec(sql, exec)
