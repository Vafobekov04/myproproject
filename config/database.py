import mysql.connector
from config.settings import DATABASE


class Database:

    @staticmethod
    def get_connection():

        try:

            connection = mysql.connector.connect(
                host=DATABASE["host"],
                user=DATABASE["user"],
                password=DATABASE["password"],
                database=DATABASE["database"]
            )

            return connection

        except Exception as error:

            print(error)

            return None