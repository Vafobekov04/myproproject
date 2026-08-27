import mysql.connector


class ProductRepository:

    def __init__(self, connection):
        self.connection = connection

    # =========================
    # PRODUCTS
    # =========================

    def get_products(self):
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.product_id,
                p.product_name,
                p.price,
                p.quantity,
                p.status,
                p.category_id,
                c.category_name
            FROM Products p
            LEFT JOIN Categories c ON p.category_id = c.category_id
        """)

        return cursor.fetchall()

    def search_products(self, keyword):
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.product_id,
                p.product_name,
                p.price,
                p.quantity,
                p.status,
                p.category_id,
                c.category_name
            FROM Products p
            LEFT JOIN Categories c ON p.category_id = c.category_id
            WHERE p.product_name LIKE %s
        """, (f"%{keyword}%",))

        return cursor.fetchall()

    def add_product(self, product_name, price, quantity, category_id, status):
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO Products (product_name, price, quantity, category_id, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (product_name, price, quantity, category_id, status))

        self.connection.commit()

    def update_product(self, product_id, product_name, price, quantity, category_id, status):
        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE Products
            SET product_name = %s,
                price = %s,
                quantity = %s,
                category_id = %s,
                status = %s
            WHERE product_id = %s
        """, (product_name, price, quantity, category_id, status, product_id))

        self.connection.commit()

    def delete_product(self, product_id):
        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM Products WHERE product_id = %s
        """, (product_id,))

        self.connection.commit()

    # =========================
    # CATEGORIES
    # =========================

    def get_categories(self):
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT category_id, category_name FROM Categories
        """)

        return cursor.fetchall()

    def filter_by_category(self, category_id):
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                p.product_id,
                p.product_name,
                p.price,
                p.quantity,
                p.status,
                p.category_id,
                c.category_name
            FROM Products p
            LEFT JOIN Categories c ON p.category_id = c.category_id
            WHERE p.category_id = %s
        """, (category_id,))

        return cursor.fetchall()

    def add_category(self, category_name):
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO Categories (category_name)
            VALUES (%s)
        """, (category_name,))

        self.connection.commit()
        return cursor.lastrowid

    def delete_category(self, category_id):
        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM Categories WHERE category_id = %s
        """, (category_id,))

        self.connection.commit()

    def update_category(self, category_id, category_name):
        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE Categories
            SET category_name = %s
            WHERE category_id = %s
        """, (category_name, category_id))

        self.connection.commit()