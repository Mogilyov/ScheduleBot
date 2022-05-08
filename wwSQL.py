import sqlite3


class SQL:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `subscriptions` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, username, status=True, group=None):
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`, `group`, username) VALUES(?,?,?,?)", (user_id, status, group, username))

    def update_subscription(self, user_id, status):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def set_group(self, user_id, group):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `group` = ? WHERE `user_id` = ?", (group, user_id))

    def set_language(self, user_id, language):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `language` = ? WHERE `user_id` = ?", (language, user_id))

    def get_subscriber_language(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `language` FROM `subscriptions` WHERE `user_id` = ?", (user_id,)).fetchall()

    def close(self):
        self.connection.close()
