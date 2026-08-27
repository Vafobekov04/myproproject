from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QMessageBox, QLabel, QFrame
)
from PyQt6.QtCore import Qt

from business.client_service import ClientService


class ClientWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.service = ClientService()

        self.setWindowTitle("Клиенты")
        self.resize(1000, 650)

        self.selected_client_id = None

        self.setStyleSheet(self.styles())

        self.init_ui()
        self.load_data()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # ===== TITLE =====
        title = QLabel("👥 Управление клиентами")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")

        # ===== SEARCH =====
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск клиента...")
        self.search_input.textChanged.connect(self.search)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "ID", "ФИО", "Телефон", "Email"
        ])
        self.table.cellClicked.connect(self.select_row)

        # ===== FORM =====
        form = QFrame()
        form.setObjectName("card")

        form_layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("ФИО")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Телефон")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Адрес (необязательно)")

        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.phone_input)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.address_input)

        form.setLayout(form_layout)

        # ===== BUTTONS =====
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add_client)

        update_btn = QPushButton("Обновить")
        update_btn.clicked.connect(self.update_client)

        delete_btn = QPushButton("Удалить")
        delete_btn.clicked.connect(self.delete_client)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(update_btn)
        btn_layout.addWidget(delete_btn)

        # ===== LAYOUT =====
        main_layout.addWidget(title)
        main_layout.addWidget(self.search_input)
        main_layout.addWidget(self.table)
        main_layout.addWidget(form)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    # ================= DATA =================

    def load_data(self):
        data = self.service.get_clients()
        self.fill_table(data)

    def fill_table(self, data):

        self.table.setRowCount(len(data))

        for row, client in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(client["client_id"])))
            self.table.setItem(row, 1, QTableWidgetItem(client["full_name"]))
            self.table.setItem(row, 2, QTableWidgetItem(client["phone"]))
            self.table.setItem(row, 3, QTableWidgetItem(client["email"]))

    # ================= SEARCH =================

    def search(self):

        keyword = self.search_input.text()

        if keyword == "":
            self.load_data()
        else:
            data = self.service.search_clients(keyword)
            self.fill_table(data)

    # ================= SELECT =================

    def select_row(self, row):

        self.selected_client_id = int(self.table.item(row, 0).text())

        self.name_input.setText(self.table.item(row, 1).text())
        self.phone_input.setText(self.table.item(row, 2).text())
        self.email_input.setText(self.table.item(row, 3).text())

    # ================= ACTIONS =================

    def add_client(self):

        result = self.service.add_client(
        self.name_input.text(),
               self.phone_input.text(),
            self.email_input.text(),
            self.address_input.text())

        if result == "OK":
            self.load_data()
        else:
            QMessageBox.warning(self, "Ошибка", result)

    def update_client(self):

        if not self.selected_client_id:
            return

        self.service.update_client(
            self.selected_client_id,
            self.name_input.text(),
            self.phone_input.text(),
            self.email_input.text()
        )

        self.load_data()

    def delete_client(self):

        if not self.selected_client_id:
            return

        self.service.delete_client(self.selected_client_id)
        self.load_data()

    # ================= STYLE =================

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
        }

        QLineEdit {
            padding: 8px;
            border-radius: 8px;
            background-color: #1e293b;
        }

        QTableWidget {
            background-color: #1e293b;
            border-radius: 10px;
        }

        QPushButton {
            background-color: #38bdf8;
            padding: 8px;
            border-radius: 8px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #0ea5e9;
        }

        #card {
            background-color: #1e293b;
            border-radius: 12px;
            padding: 10px;
        }
        """