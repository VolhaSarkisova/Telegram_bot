import sqlite3
from dbconnection import DBConnection
from queries import *
import datetime
import os
from dotenv import load_dotenv
load_dotenv()


class Cafe:
    def __init__(self):
        self.db_conn = DBConnection(os.getenv('DB'))
        self.db_conn.execute(create_table_hall_types())
        self.db_conn.execute(create_table_tables())
        self.db_conn.execute(create_table_reserve())
        self.db_conn.execute(create_table_hours())
        self.db_conn.execute(create_table_admins())

    def select_reserve_by_date_bool(self, date: datetime) -> bool | dict:
        try:
            self.db_conn.cursor.execute(
                select_reserve_by_date(),
                (date,)
            )
            rows: list = self.db_conn.cursor.fetchall()
            if rows == []:
                return False
            else:
                return True
        except sqlite3.OperationalError as err:
            return {"err_message": err}
    def insert_reserve_by_date(self, date: datetime) -> None | dict:
        try:
            self.db_conn.cursor.execute(
                insert_reserve_by_date(),
                (str(date),)
            )
            self.db_conn.conn.commit()
        except sqlite3.OperationalError as err:
            return {"err_message": err}
    def select_unreserved_hours_by_date(self, date: datetime, hour: int, duration: int) -> list | dict:
        try:
            self.db_conn.cursor.execute(
                select_unreserved_hours_by_date(),
                (date, hour, duration)
            )
            rows: list = self.db_conn.cursor.fetchall()
            return rows
        except sqlite3.OperationalError as err:
            return {"err_message": err}
    def select_unreserved_tables_by_date_duration_hour(self, date: datetime, hour: int, duration: int) -> list | dict:
        try:
            upper_hour: int = hour + duration
            self.db_conn.cursor.execute(
                select_unreserved_tables_by_date_duration_hour(),
                (date, hour, upper_hour, duration+1)
            )
            rows: list = self.db_conn.cursor.fetchall()
            return rows
        except sqlite3.OperationalError as err:
            return {"err_message": err}
    def select_table_by_id(self, id: int) -> list | dict:
        try:
            self.db_conn.cursor.execute(
                select_table_by_id(),
                (id, )
            )
            return self.db_conn.cursor.fetchone()
        except sqlite3.OperationalError as err:
            return {"err_message": err}
    def update_reserve_client_by_id_table_date_hour(self, date: datetime, id_table: int, hour: int, client: int, client_id: int, reserved: int) -> None | dict:
        try:
            self.db_conn.cursor.execute(
                update_reserve_client_by_id_table_date_hour(),
                (client, client_id, reserved, id_table, date, hour)
            )
            self.db_conn.conn.commit()
        except sqlite3.OperationalError as err:
            return {"err_message": err}
    def select_admins_client_id(self) -> bool | dict:
        try:
            self.db_conn.cursor.execute(
                select_admins_client_id(),
                ()
            )
            rows: list = self.db_conn.cursor.fetchall()
            return rows
        except sqlite3.OperationalError as err:
            return {"err_message": err}
    def select_admins_username_by_client_id(self, client_id: int) -> bool | dict:
        try:
            self.db_conn.cursor.execute(
                select_admins_username_by_client_id(),
                (client_id, )
            )
            return self.db_conn.cursor.fetchone()
        except sqlite3.OperationalError as err:
            return {"err_message": err}




