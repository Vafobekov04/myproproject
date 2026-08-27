import mysql.connector


def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sales_system",
            port=3306
        )
    except mysql.connector.Error as err:
        print(f"Ошибка подключения к БД: {err}")
        return None