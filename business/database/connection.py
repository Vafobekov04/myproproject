import mysql.connector

_conn = None

def get_connection():
    global _conn

    if _conn is None:
        _conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",   # твой пароль MySQL
            database="sales_system"
        )

    return _conn