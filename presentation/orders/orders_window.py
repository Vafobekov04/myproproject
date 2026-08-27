from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QFrame,
    QMessageBox, QComboBox, QHeaderView
)
from PyQt6.QtCore import Qt

from business.order_service import OrderService
from business.client_service import ClientService

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors


class OrderWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.service = OrderService()
        self.client_service = ClientService()

        self.setWindowTitle("Заказы")
        self.resize(1000, 650)

        self.selected_id = None

        self.setStyleSheet(self.styles())

        self.init_ui()
        self.load_data()

    # ================= UI =================

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        title = QLabel("📦 Управление заказами")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")

        # ===== FORM =====
        form = QFrame()
        form.setObjectName("card")

        form_layout = QVBoxLayout()

        self.client_box = QComboBox()
        self.employee_input = QLineEdit()
        self.employee_input.setPlaceholderText("ID сотрудника")

        self.total_input = QLineEdit()
        self.total_input.setPlaceholderText("Сумма заказа")

        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Статус (new / done / cancel)")

        form_layout.addWidget(self.client_box)
        form_layout.addWidget(self.employee_input)
        form_layout.addWidget(self.total_input)
        form_layout.addWidget(self.status_input)

        form.setLayout(form_layout)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Клиент",
            "Сотрудник",
            "Дата",
            "Сумма",
            "Статус",
            "Товары"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.cellClicked.connect(self.select_row)

        # ===== BUTTONS =====
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add)

        delete_btn = QPushButton("Удалить")
        delete_btn.clicked.connect(self.delete)

        pdf_btn = QPushButton("PDF документ")
        pdf_btn.clicked.connect(self.generate_pdf)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(pdf_btn)

        # ===== LAYOUT =====
        main_layout.addWidget(title)
        main_layout.addWidget(form)
        main_layout.addWidget(self.table)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    # ================= CLIENTS =================

    def load_clients(self):

        clients = self.client_service.get_clients()

        self.client_box.clear()

        for client in clients:
            self.client_box.addItem(
                client["full_name"],
                client["id"] if "id" in client else client["client_id"]
            )

    # ================= DATA =================

    def load_data(self):

        self.load_clients()

        data = self.service.get_orders()

        self.table.setRowCount(len(data))

        for i, o in enumerate(data):

            order_id = o["id"] if "id" in o else o["order_id"]

            self.table.setItem(i, 0, QTableWidgetItem(str(order_id)))
            self.table.setItem(i, 1, QTableWidgetItem(str(o["client_id"])))
            self.table.setItem(i, 2, QTableWidgetItem(str(o["employee_id"])))
            self.table.setItem(i, 3, QTableWidgetItem(str(o["order_date"])))
            self.table.setItem(i, 4, QTableWidgetItem(str(o["total_amount"])))
            self.table.setItem(i, 5, QTableWidgetItem(o["status"]))

            items_text = self.service.get_order_items_text(order_id)
            self.table.setItem(i, 6, QTableWidgetItem(items_text))

    # ================= SELECT =================

    def select_row(self, row):

        self.selected_id = int(
            self.table.item(row, 0).text()
        )

    # ================= ACTIONS =================

    def add(self):

        self.service.add_order(
            self.client_box.currentData(),
            self.employee_input.text(),
            self.total_input.text(),
            self.status_input.text()
        )

        self.load_data()

        QMessageBox.information(self, "Успешно", "Заказ добавлен")

    def delete(self):

        if not self.selected_id:
            return

        self.service.delete_order(self.selected_id)

        self.load_data()

        QMessageBox.information(self, "Успешно", "Заказ удален")

    # ================= PDF =================

    def generate_pdf(self):

        if not self.selected_id:
            return

        order = next(
            (o for o in self.service.get_orders()
             if (o["id"] if "id" in o else o["order_id"]) == self.selected_id),
            None
        )

        if not order:
            return

        order_id = self.selected_id
        items = self.service.get_order_items(order_id)

        file_name = f"order_{order_id}.pdf"

        c = canvas.Canvas(file_name, pagesize=A4)
        width, height = A4

        # HEADER
        c.setFont("Helvetica-Bold", 20)
        c.drawString(150, height - 70, "SALES SYSTEM ORDER")

        # ORDER INFO
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 120, f"Order ID: {order_id}")
        c.drawString(50, height - 140, f"Client ID: {order['client_id']}")
        c.drawString(50, height - 160, f"Employee ID: {order['employee_id']}")
        c.drawString(50, height - 180, f"Date: {order['order_date']}")
        c.drawString(50, height - 200, f"Status: {order['status']}")

        # ITEMS HEADER
        y = height - 260

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Products:")

        y -= 30

        c.setFont("Helvetica", 11)

        for item in items:
            c.drawString(60, y,
                         f"{item['product_name']} x{item['quantity']} - {item['price']} $")
            y -= 20

        # TOTAL
        y -= 30
        c.setFont("Helvetica-Bold", 14)
        c.drawString(60, y, f"TOTAL: {order['total_amount']} $")

        c.save()

        QMessageBox.information(
            self,
            "PDF",
            f"Файл создан: {file_name}"
        )

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

        QLineEdit, QComboBox {
            background-color: #1e293b;
            padding: 8px;
            border-radius: 8px;
        }

        QTableWidget {
            background-color: #1e293b;
            border-radius: 10px;
        }

        QPushButton {
            background-color: #38bdf8;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #0ea5e9;
        }

        #card {
            background-color: #1e293b;
            padding: 10px;
            border-radius: 10px;
        }
        """