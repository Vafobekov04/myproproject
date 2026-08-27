class ClientRepository:

    def __init__(self, connection):
        self.connection = connection

    # ===== GET ALL =====
    def get_all(self):

        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT client_id, full_name, phone, email
            FROM clients
        """)

        result = cursor.fetchall()
        cursor.close()

        return result

    # ===== SEARCH =====
    def search(self, keyword):

        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT client_id, full_name, phone, email
            FROM clients
            WHERE full_name LIKE %s
               OR phone LIKE %s
               OR email LIKE %s
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

        result = cursor.fetchall()
        cursor.close()

        return result

    # ===== ADD =====
    def add(self, full_name, phone, email, address):

     cursor = self.connection.cursor()

     cursor.execute("""
        INSERT INTO clients (full_name, phone, email, address)
        VALUES (%s, %s, %s, %s)
    """, (full_name, phone, email, address))

     self.connection.commit()
     cursor.close()

    # ===== UPDATE =====
    def update(self, client_id, full_name, phone, email):

        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE clients
            SET full_name=%s, phone=%s, email=%s
            WHERE client_id=%s
        """, (full_name, phone, email, client_id))

        self.connection.commit()
        cursor.close()

    # ===== DELETE =====
    def delete(self, client_id):

        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM clients
            WHERE client_id=%s
        """, (client_id,))

        self.connection.commit()
        cursor.close()