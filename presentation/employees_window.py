from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QMessageBox, QFrame,
    QLineEdit
)
from PyQt6.QtCore import Qt

from business.employee_service import EmployeeService


class EmployeeWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.service = EmployeeService()

        self.setWindowTitle("Управление сотрудниками")
        self.resize(1000, 700)

        self.selected_employee_id = None

        self.setStyleSheet(self.styles())

        self.init_ui()
        self.load_data()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # ===== TITLE =====
        title = QLabel("👥 Управление сотрудниками")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")

        # ===== FORM CARD =====
        form = QFrame()
        form.setObjectName("card")

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        # Full name input
        name_label = QLabel("ФИ сотрудника:")
        name_label.setObjectName("formLabel")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите полное имя")
        self.name_input.setObjectName("formInput")

        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)

        # Position input
        position_label = QLabel("Должность:")
        position_label.setObjectName("formLabel")
        self.position_input = QLineEdit()
        self.position_input.setPlaceholderText("Введите должность")
        self.position_input.setObjectName("formInput")

        form_layout.addWidget(position_label)
        form_layout.addWidget(self.position_input)

        form.setLayout(form_layout)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "ID", "ФИ", "Должность"
        ])
        self.table.setObjectName("employeeTable")
        self.table.cellClicked.connect(self.select_row)
        self.table.horizontalHeader().setStretchLastSection(True)

        # ===== BUTTONS =====
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        add_btn = QPushButton("➕ Добавить сотрудника")
        add_btn.setObjectName("btnAdd")
        add_btn.clicked.connect(self.add)

        update_btn = QPushButton("✏️ Обновить сотрудника")
        update_btn.setObjectName("btnUpdate")
        update_btn.clicked.connect(self.update)

        delete_btn = QPushButton("🗑️ Удалить сотрудника")
        delete_btn.setObjectName("btnDelete")
        delete_btn.clicked.connect(self.delete)

        clear_btn = QPushButton("🔄 Очистить форму")
        clear_btn.setObjectName("btnClear")
        clear_btn.clicked.connect(self.clear_form)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(update_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()

        # ===== LAYOUT =====
        main_layout.addWidget(title)
        main_layout.addWidget(form)
        main_layout.addWidget(self.table)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    # ================= LOAD DATA =================

    def load_data(self):
        """Load and display all employees"""
        try:
            data = self.service.get_employees()
            self.table.setRowCount(len(data))

            for i, employee in enumerate(data):
                self.table.setItem(i, 0, QTableWidgetItem(str(employee.get("employee_id", "—"))))
                self.table.setItem(i, 1, QTableWidgetItem(str(employee.get("full_name", "—"))))
                self.table.setItem(i, 2, QTableWidgetItem(str(employee.get("position", "—"))))
        except Exception as e:
            print(f"Error loading employees: {e}")
            QMessageBox.warning(self, "Ошибка", f"Ошибка загрузки сотрудников: {str(e)}")

    # ================= SELECT =================

    def select_row(self, row):
        """Select employee from table and populate form"""
        try:
            self.selected_employee_id = int(self.table.item(row, 0).text())
            full_name = self.table.item(row, 1).text()
            position = self.table.item(row, 2).text()
            
            self.name_input.setText(full_name)
            self.position_input.setText(position)
        except (ValueError, AttributeError):
            self.selected_employee_id = None

    # ================= ACTIONS =================

    def add(self):
        """Add new employee"""
        full_name = self.name_input.text()
        position = self.position_input.text()

        if not full_name or not position:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        result = self.service.add_employee(full_name, position)
        
        if result == "OK":
            self.clear_form()
            self.load_data()
            QMessageBox.information(self, "Успешно", "Сотрудник добавлен!")
        else:
            QMessageBox.warning(self, "Ошибка", result)

    def update(self):
        """Update selected employee"""
        if not self.selected_employee_id:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для обновления!")
            return

        full_name = self.name_input.text()
        position = self.position_input.text()

        if not full_name or not position:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        result = self.service.update_employee(self.selected_employee_id, full_name, position)
        
        if result == "OK":
            self.clear_form()
            self.load_data()
            QMessageBox.information(self, "Успешно", "Сотрудник обновлён!")
        else:
            QMessageBox.warning(self, "Ошибка", result)

    def delete(self):
        """Delete selected employee"""
        if not self.selected_employee_id:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для удаления!")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить этого сотрудника?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            result = self.service.delete_employee(self.selected_employee_id)
            
            if result == "OK":
                self.clear_form()
                self.load_data()
                QMessageBox.information(self, "Успешно", "Сотрудник удалён!")
            else:
                QMessageBox.warning(self, "Ошибка", result)

    def clear_form(self):
        """Clear input fields"""
        self.name_input.clear()
        self.position_input.clear()
        self.selected_employee_id = None

    # ================= STYLES =================

    def styles(self):
        return """
        QWidget {
            background-color: #0f172a;
            color: white;
            font-size: 14px;
        }

        #title {
            font-size: 24px;
            font-weight: bold;
            color: #f1f5f9;
        }

        #formLabel {
            font-size: 13px;
            font-weight: 600;
            color: #cbd5e1;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        #formInput {
            padding: 10px;
            border-radius: 8px;
            background-color: #1e293b;
            border: 1px solid #334155;
            color: white;
            min-height: 35px;
        }

        #formInput:hover {
            border: 1px solid #475569;
        }

        #formInput:focus {
            border: 1px solid #38bdf8;
        }

        #employeeTable {
            background-color: #1e293b;
            border-radius: 10px;
            border: 1px solid #334155;
            gridline-color: #334155;
        }

        QTableWidget::item {
            padding: 8px;
            color: #cbd5e1;
        }

        QTableWidget::item:selected {
            background-color: #334155;
        }

        QHeaderView::section {
            background-color: #1e293b;
            color: #cbd5e1;
            padding: 10px;
            border: none;
            font-weight: bold;
            font-size: 13px;
        }

        #btnAdd {
            background-color: #10b981;
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-weight: bold;
            border: none;
        }

        #btnAdd:hover {
            background-color: #059669;
        }

        #btnUpdate {
            background-color: #3b82f6;
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-weight: bold;
            border: none;
        }

        #btnUpdate:hover {
            background-color: #2563eb;
        }

        #btnDelete {
            background-color: #ef4444;
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-weight: bold;
            border: none;
        }

        #btnDelete:hover {
            background-color: #dc2626;
        }

        #btnClear {
            background-color: #8b5cf6;
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-weight: bold;
            border: none;
        }

        #btnClear:hover {
            background-color: #7c3aed;
        }

        #card {
            background-color: #1e293b;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #334155;
        }
        """
