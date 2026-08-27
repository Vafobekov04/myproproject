class EmployeeRepository:

    def __init__(self, connection):
        self.connection = connection

    def get_all(self):
        """Get all employees"""
        cursor = self.connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT employee_id, full_name, position
            FROM Employees
            ORDER BY employee_id DESC
        """)

        result = cursor.fetchall()
        cursor.close()
        return result

    def add(self, full_name, position):
        """Add new employee"""
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO Employees (full_name, position)
            VALUES (%s, %s)
        """, (full_name, position))

        self.connection.commit()
        cursor.close()

    def update(self, employee_id, full_name, position):
        """Update employee information"""
        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE Employees 
            SET full_name = %s, position = %s
            WHERE employee_id = %s
        """, (full_name, position, employee_id))

        self.connection.commit()
        cursor.close()

    def delete(self, employee_id):
        """Delete employee"""
        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM Employees WHERE employee_id = %s
        """, (employee_id,))

        self.connection.commit()
        cursor.close()
