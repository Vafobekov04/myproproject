import mysql.connector


def create_database():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345"
    )

    cursor = connection.cursor()

    try:

        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS sales_system"
        )

        print("База данных создана")

    except Exception as error:

        print(
            f"Ошибка: {error}"
        )

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":

    create_database()