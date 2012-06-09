import MySQLdb as mdb


class TransitDB:

    def __init__(self):
        self.conn = mdb.connect('50.57.65.176', 'transit', 'mtlhack', 'transit')
        self.cursor = self.conn.cursor()

    def run(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def get_one(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def get_all(self, sql):
        self.cursor.execute(sql)
        while 1:
            try:
                data = self.cursor.fetchone()
                if data is None:
                    raise Exception("Done!")
                yield data
            except:
                break
