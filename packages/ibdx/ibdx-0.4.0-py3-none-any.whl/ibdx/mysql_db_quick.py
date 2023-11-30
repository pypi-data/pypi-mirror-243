from pymysql import connect


class MysqlConn:
    def __init__(self, db: str, host='127.0.0.1', port=3306, user='root', password=''):
        self.conn = connect(host=host, port=port, user=user, password=password, database=db)
        self.db = db

    def __enter__(self):
        return self

    def __exit__(self, **exc_info):
        self.conn.close()

    def query(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        return cursor

    def get_tables(self) -> list[str]:
        with self.query('show tables') as cur:
            return [rs_tup[0] for rs_tup in cur]

    def get_version(self) -> str:
        with self.query('select version()') as cur:
            if res := cur.fetchone():
                return res[0]
            else:
                raise Exception("failed to read server's version.")
