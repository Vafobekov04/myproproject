from data.database import get_connection


class DashboardService:

    def __init__(self):

        self.connection = get_connection()

    def get_statistics(self):

        cursor = self.connection.cursor(dictionary=True)

        # клиенты
        cursor.execute(
            "SELECT COUNT(*) AS count FROM Clients"
        )

        clients = cursor.fetchone()["count"]

        # товары
        cursor.execute(
            "SELECT COUNT(*) AS count FROM Products"
        )

        products = cursor.fetchone()["count"]

        # заказы
        cursor.execute(
            "SELECT COUNT(*) AS count FROM Orders"
        )

        orders = cursor.fetchone()["count"]

        # сумма продаж
        cursor.execute(
            "SELECT IFNULL(SUM(total_amount), 0) AS total FROM Orders"
        )

        total = cursor.fetchone()["total"]

        return {
            "clients": clients,
            "products": products,
            "orders": orders,
            "total": total
        }