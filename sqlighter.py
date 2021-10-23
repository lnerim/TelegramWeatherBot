import sqlite3


class SQLighter:
    def __init__(self, database):
        """Подключние к БД и сохранение курсора соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

        with self.connection:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS sub ("
                                "id integer PRIMARY KEY, "
                                "user_id integer NOT NULL, "
                                "city text, "
                                "status blob NOT NULL);")

    def get_subs(self, status=True):
        """Получение всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `sub` WHERE `status` = ?", (status,)).fetchall()

    def check_subs(self, user_id):
        """Проверка на наличие пользователя в базе"""
        with self.connection:
            result = self.cursor.execute("SELECT `status` FROM `sub` WHERE `user_id` = ?", (user_id,)).fetchone()
            return bool(result[0])

    def add_subs(self, user_id, city, status=True):
        """Добавление нового подписчика"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `sub` (`user_id`, `city`, `status`) VALUES(?,?,?)", (user_id, city, status))

    def upd_subs(self, user_id, city=None, status=True):
        """Обновление статуса подписки пользователя"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE `sub` SET `status` = ?, `city` = ? WHERE `user_id` = ?", (status, city, user_id))


if __name__ == "__main__":
    s = SQLighter(":memory:")
