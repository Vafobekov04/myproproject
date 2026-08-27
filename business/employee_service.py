from data.database import get_connection
from data.repositories.employee_repository import EmployeeRepository


class EmployeeService:

    def __init__(self):
        self.connection = get_connection()
        self.repo = EmployeeRepository(self.connection)

    def get_employees(self):
        """Get all employees"""
        return self.repo.get_all()

    def add_employee(self, full_name, position):
        """Add new employee with validation"""
        
        if not full_name or full_name.strip() == "":
            return "ФИ сотрудника обязательно"
        
        if not position or position.strip() == "":
            return "Должность обязательна"
        
        try:
            self.repo.add(full_name.strip(), position.strip())
            return "OK"
        except Exception as e:
            return f"Ошибка добавления: {str(e)}"

    def update_employee(self, employee_id, full_name, position):
        """Update employee with validation"""
        
        if not full_name or full_name.strip() == "":
            return "ФИ сотрудника обязательно"
        
        if not position or position.strip() == "":
            return "Должность обязательна"
        
        try:
            self.repo.update(employee_id, full_name.strip(), position.strip())
            return "OK"
        except Exception as e:
            return f"Ошибка обновления: {str(e)}"

    def delete_employee(self, employee_id):
        """Delete employee"""
        try:
            self.repo.delete(employee_id)
            return "OK"
        except Exception as e:
            return f"Ошибка удаления: {str(e)}"
