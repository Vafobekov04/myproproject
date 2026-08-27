class OrderRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):

        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT order_id, client_id, employee_id, order_date, total_amount, status
            FROM orders
        """)

        result = cursor.fetchall()
        cursor.close()
        return result

    def add(self, client_id, employee_id, total_amount, status):

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO orders (client_id, employee_id, total_amount, status)
            VALUES (%s, %s, %s, %s)
        """, (client_id, employee_id, total_amount, status))

        self.connection.commit()
        cursor.close()

    def delete(self, order_id):

        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM orders WHERE order_id = %s
        """, (order_id,))

        self.connection.commit()
        cursor.close()