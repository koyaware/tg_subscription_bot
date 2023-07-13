import sqlite3
import time


class Database:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users ('user_id') VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_time_sub(self, user_id, time_sub):
        with self.connection:
            return self.cursor.execute("UPDATE users SET time_sub = ? WHERE user_id = ?", (time_sub, user_id,))

    def get_time_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT time_sub FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            return time_sub

    def get_sub_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT time_sub FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])

            if time_sub > int(time.time()):
                return True
            else:
                return False
