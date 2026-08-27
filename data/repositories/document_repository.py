class DocumentRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):

        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT document_id, order_id, document_type, create_date, file_path
            FROM Documents
        """)

        result = cursor.fetchall()
        cursor.close()
        return result

    def add(self, order_id, document_type, file_path):

        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO Documents (order_id, document_type, file_path)
            VALUES (%s, %s, %s)
        """, (order_id, document_type, file_path))

        self.connection.commit()
        cursor.close()

    def delete(self, document_id):

        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM Documents WHERE document_id = %s
        """, (document_id,))

        self.connection.commit()
        cursor.close()