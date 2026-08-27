from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QComboBox,
    QLabel, QFrame
)
from PyQt6.QtCore import Qt

from business.product_service import ProductService


class ProductWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.service = ProductService()

        self.setWindowTitle("Товары")
        self.resize(1100, 700)

        self.selected_id = None

        self.setStyleSheet(self.styles())

        self.init_ui()
        self.load_data()

    # ================= UI =================

    def init_ui(self):

        main = QVBoxLayout()
        main.setContentsMargins(20, 20, 20, 20)
        main.setSpacing(15)

        # ===== TITLE =====
        title = QLabel("📦 Управление товарами")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")

        # ===== SEARCH CARD =====
        search_card = QFrame()
        search_card.setObjectName("card")

        search_layout = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Поиск товара...")
        self.search.textChanged.connect(self.search_data)

        self.category_filter = QComboBox()
        self.category_filter.setPlaceholderText("Фильтр по категориям")
        self.category_filter.currentIndexChanged.connect(self.apply_filter)

        search_layout.addWidget(self.search)
        search_layout.addWidget(self.category_filter)
        search_card.setLayout(search_layout)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Название", "Цена", "Кол-во", "Категория", "Статус"]
        )
        self.table.cellClicked.connect(self.select)

        # ===== FORM CARD =====
        form = QFrame()
        form.setObjectName("card")

        form_layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Название товара")

        self.price = QLineEdit()
        self.price.setPlaceholderText("Цена")

        self.quantity = QLineEdit()
        self.quantity.setPlaceholderText("Количество")

        self.category = QComboBox()

        form_layout.addWidget(self.name)
        form_layout.addWidget(self.price)
        form_layout.addWidget(self.quantity)
        form_layout.addWidget(self.category)

        form.setLayout(form_layout)

        # ===== BUTTONS =====
        btns = QHBoxLayout()

        add = QPushButton("➕ Добавить")
        add.clicked.connect(self.add)

        update = QPushButton("✏️ Обновить")
        update.clicked.connect(self.update)

        delete = QPushButton("🗑 Удалить")
        delete.clicked.connect(self.delete)

        btns.addWidget(add)
        btns.addWidget(update)
        btns.addWidget(delete)

        # ===== ADD TO MAIN =====
        main.addWidget(title)
        main.addWidget(search_card)
        main.addWidget(self.table)
        main.addWidget(form)
        main.addLayout(btns)

        self.setLayout(main)

    # ================= DATA =================

    def load_data(self):
        self.fill(self.service.get_products())
        self.load_categories()

    def load_categories(self):
        cats = self.service.get_categories()
        
        self.category.clear()
        self.category_filter.clear()
        
        self.category_filter.addItem("📋 Все категории", 0)
        
        for c in cats:
            self.category.addItem(c["category_name"], c["category_id"])
            self.category_filter.addItem(c["category_name"], c["category_id"])

    def fill(self, data):

        self.table.setRowCount(len(data))

        for i, p in enumerate(data):

            self.table.setItem(i, 0, QTableWidgetItem(str(p["product_id"])))
            self.table.setItem(i, 1, QTableWidgetItem(p["product_name"]))
            self.table.setItem(i, 2, QTableWidgetItem(str(p["price"])))
            self.table.setItem(i, 3, QTableWidgetItem(str(p["quantity"])))
            self.table.setItem(i, 4, QTableWidgetItem(str(p["category_name"])))
            self.table.setItem(i, 5, QTableWidgetItem(str(p.get("status", "—"))))

    # ================= SEARCH =================

    def search_data(self):
        text = self.search.text()

        if not text:
            self.load_data()
        else:
            self.fill(self.service.search_products(text))

    def apply_filter(self):
        category_id = self.category_filter.currentData()
        
        if category_id == 0:
            self.load_data()
        else:
            self.fill(self.service.filter_by_category(category_id))

    # ================= SELECT =================

    def select(self, row):

        self.selected_id = int(self.table.item(row, 0).text())

        self.name.setText(self.table.item(row, 1).text())
        self.price.setText(self.table.item(row, 2).text())
        self.quantity.setText(self.table.item(row, 3).text())

    # ================= ACTIONS =================

    def add(self):

        try:
            result = self.service.add_product(
                self.name.text(),
                float(self.price.text()),
                int(self.quantity.text()),
                self.category.currentData()
            )

            if result == "OK":
                self.load_data()
                QMessageBox.information(self, "Успех", "Товар добавлен")
            else:
                QMessageBox.warning(self, "Ошибка", result)

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Цена и количество должны быть числами")

    def update(self):

        if not self.selected_id:
            return

        try:
            self.service.update_product(
                self.selected_id,
                self.name.text(),
                float(self.price.text()),
                int(self.quantity.text()),
                self.category.currentData()
            )

            self.load_data()
            QMessageBox.information(self, "Успех", "Товар обновлён")

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Цена и количество должны быть числами")

    def delete(self):

        if not self.selected_id:
            return

        self.service.delete_product(self.selected_id)
        self.load_data()

        QMessageBox.information(self, "Успех", "Товар удалён")

    # ================= STYLE =================

    def styles(self):

        return """
        QWidget {
            background-color: #0f172a;
            color: #e2e8f0;
            font-size: 14px;
        }

        #title {
            font-size: 26px;
            font-weight: bold;
            color: #38bdf8;
            margin-bottom: 10px;
        }

        #card {
            background-color: #111827;
            border-radius: 12px;
            padding: 12px;
        }

        QLineEdit, QComboBox {
            background-color: #1e293b;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #334155;
        }

        QLineEdit:focus {
            border: 1px solid #38bdf8;
        }

        QTableWidget {
            background-color: #111827;
            border-radius: 10px;
            gridline-color: #334155;
        }

        QHeaderView::section {
            background-color: #1f2937;
            padding: 6px;
            border: none;
            font-weight: bold;
            color: #93c5fd;
        }

        QPushButton {
            background-color: #38bdf8;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
            color: black;
        }

        QPushButton:hover {
            background-color: #0ea5e9;
        }
        """