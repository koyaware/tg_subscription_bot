import sqlite3
import time


class Database:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, username, full_name, reg_time):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, username, full_name, reg_time) VALUES (?, ?, ?, ?)",
                                       (user_id, username, full_name, reg_time))

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

    def set_ban_status(self, user_id, ban_status):
        with self.connection:
            try:
                user_id = int(user_id)
                return self.cursor.execute("UPDATE users SET is_ban = ? WHERE user_id = ?", (ban_status, user_id,))
            except ValueError:
                return self.cursor.execute("UPDATE users SET is_ban = ? WHERE username = ?", (ban_status, user_id,))

    def get_ban_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT is_ban FROM users WHERE user_id = ?", (user_id,)).fetchall()
            if len(result) == 0:
                return False

            for row in result:
                ban_status = int(row[0])

            if ban_status > 0:
                return True
            else:
                return False

    def get_ban_users(self):
        with self.connection:
            self.cursor.execute("SELECT user_id, username, full_name FROM users WHERE is_ban = 1")
            banned_users = self.cursor.fetchall()

            if len(banned_users) == 0:
                return False

            formatted_users = []
            for user in banned_users:
                user_id = user[0]
                username = user[1]
                full_name = user[2]
                formatted_user = f"ID пользователя: {user_id}\n@username пользователя: @{username}\nИмя пользователя: {full_name}\n"
                formatted_users.append(formatted_user)

            return formatted_users
