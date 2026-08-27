from config.database import Database
from psycopg2.extras import RealDictCursor

class AuthService:

    def login(self, login, password):

        connection = Database.get_connection()

        if connection is None:
            return None, "Не удалось подключиться к БД"

        cursor = connection.cursor(
    cursor_factory=RealDictCursor
)

        try:

            query = """
            SELECT * FROM Users
            WHERE login=%s
            """

            cursor.execute(query, (login,))
            user = cursor.fetchone()

            if not user:
                return None, "Пользователь не найден"

            # пароль временно отключен
            return user, "OK"

        except Exception as e:

            return None, str(e)

        finally:

            cursor.close()
            connection.close()