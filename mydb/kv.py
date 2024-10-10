import sqlite3
import os


class Kv:
    def __init__(self):
        dbpath = os.path.expanduser("~") + "/.my.db"
        self.conn = sqlite3.connect(dbpath)
        self.cur = self.conn.cursor()

        # for short code
        self.commit = self.conn.commit
        self.execute = self.cur.execute

        # init db file
        self.initDataBase()

    def __del__(self):
        self.conn.close()

    def initDataBase(self):
        self.execute(
            """
        CREATE TABLE IF NOT EXISTS kv_store (
            key TEXT PRIMARY KEY,
            value BLOB
        )
        """
        )
        self.commit()

    def insert(self, k, v):
        self.execute("INSERT INTO kv_store (key, value) VALUES (?, ?)", (k, v))

    def update(self, k, v):
        self.execute("UPDATE kv_store SET value = ? WHERE key = ?", (v, k))

    def move(self, fromK, toK):
        self.execute("UPDATE kv_store SET key = ? WHERE key = ?", (toK, fromK))

    def put(self, k, v):
        try:
            self.insert(k, v)
        except sqlite3.IntegrityError:
            self.update(k, v)

    def delete(self, k):
        self.execute("DELETE FROM kv_store WHERE key = ?", (k,))

    def get(self, k):
        self.execute("SELECT value FROM kv_store WHERE key = ?", (k,))
        result = self.cur.fetchone()
        return result

    def test_show(self):
        result = self.execute("SELECT * FROM kv_store").fetchall()
        print(("key", "value"))
        for row in result:
            print(row)
