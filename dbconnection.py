
import sqlite3
from sqlite3 import Connection, Cursor


class DBConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn: Connection = sqlite3.connect(self.db_name)
        self.cursor: Cursor = self.conn.cursor()

    def execute(self, query):
        self.cursor.execute(query)

    def close_cursor(self):
        self.cursor.close()

    def close_connection(self):
        self.conn.close()