from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QMessageBox, QFrame,
    QComboBox
)
from PyQt6.QtCore import Qt

from business.document_service import DocumentService
from business.order_service import OrderService


class DocumentWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.service = DocumentService()
        self.order_service = OrderService()

        self.setWindowTitle("Управление документами")
        self.resize(1100, 700)

        self.selected_doc_id = None
        self.selected_order_id = None

        self.setStyleSheet(self.styles())

        self.init_ui()
        self.load_data()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # ===== TITLE =====
        title = QLabel("📄 Управление документами")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")

        # ===== FORM CARD =====
        form = QFrame()
        form.setObjectName("card")

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        # Order selection
        order_label = QLabel("Выберите заказ:")
        order_label.setObjectName("formLabel")
        self.order_combo = QComboBox()
        self.order_combo.setObjectName("formCombo")
        self.load_orders_combo()
        
        form_layout.addWidget(order_label)
        form_layout.addWidget(self.order_combo)

        # Document type selection
        type_label = QLabel("Тип документа:")
        type_label.setObjectName("formLabel")
        self.type_combo = QComboBox()
        self.type_combo.setObjectName("formCombo")
        self.type_combo.addItems([
            "Order",         # Профессиональный заказ (NEW)
            "Contract",      # Контракт
            "Invoice",       # Счёт-фактура
            "Receipt",       # Квитанция
            "Act",          # Акт
            "Check"         # Чек
        ])
        
        form_layout.addWidget(type_label)
        form_layout.addWidget(self.type_combo)

        form.setLayout(form_layout)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID документа", "ID заказа", "Клиент", "Тип", "Дата создания", "Файл"
        ])
        self.table.setObjectName("documentTable")
        self.table.cellClicked.connect(self.select_row)
        self.table.horizontalHeader().setStretchLastSection(True)

        # ===== BUTTONS =====
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        add_btn = QPushButton("✅ Сгенерировать документ")
        add_btn.setObjectName("btnAdd")
        add_btn.clicked.connect(self.add)

        delete_btn = QPushButton("🗑️ Удалить документ")
        delete_btn.setObjectName("btnDelete")
        delete_btn.clicked.connect(self.delete)

        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.setObjectName("btnRefresh")
        refresh_btn.clicked.connect(self.load_data)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()

        # ===== LAYOUT =====
        main_layout.addWidget(title)
        main_layout.addWidget(form)
        main_layout.addWidget(self.table)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    # ================= LOAD DATA =================

    def load_orders_combo(self):
        """Load orders into combo box"""
        try:
            orders = self.order_service.get_orders()
            self.order_combo.clear()
            
            if orders:
                self.order_combo.addItem("-- Выберите заказ --", None)
                for order in orders:
                    order_id = order.get('order_id') or order.get('id')
                    display_text = f"Заказ #{order_id}"
                    self.order_combo.addItem(display_text, order_id)
            else:
                self.order_combo.addItem("-- Нет доступных заказов --", None)
        except Exception as e:
            print(f"Error loading orders: {e}")
            self.order_combo.addItem("-- Ошибка загрузки --", None)

    def load_data(self):
        """Load and display all documents"""
        try:
            data = self.service.get_documents_with_client_info()
            self.table.setRowCount(len(data))

            for i, doc in enumerate(data):
                self.table.setItem(i, 0, QTableWidgetItem(str(doc.get("document_id", "—"))))
                self.table.setItem(i, 1, QTableWidgetItem(str(doc.get("order_id", "—"))))
                self.table.setItem(i, 2, QTableWidgetItem(str(doc.get("client_name", "—"))))
                self.table.setItem(i, 3, QTableWidgetItem(str(doc.get("document_type", "—"))))
                self.table.setItem(i, 4, QTableWidgetItem(str(doc.get("create_date", "—"))))
                self.table.setItem(i, 5, QTableWidgetItem(str(doc.get("file_path", "—"))))
        except Exception as e:
            print(f"Error loading documents: {e}")
            QMessageBox.warning(self, "Ошибка", f"Ошибка загрузки документов: {str(e)}")

    # ================= SELECT =================

    def select_row(self, row):
        """Select document from table"""
        try:
            self.selected_doc_id = int(self.table.item(row, 0).text())
        except ValueError:
            self.selected_doc_id = None

    # ================= ACTIONS =================

    def add(self):
        """Add new document with PDF generation"""
        order_id = self.order_combo.currentData()
        if order_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ!")
            return

        document_type = self.type_combo.currentText()
        if not document_type:
            QMessageBox.warning(self, "Ошибка", "Выберите тип документа!")
            return

        try:
            result = self.service.add_document(order_id, document_type)

            if result == "OK":
                QMessageBox.information(
                    self,
                    "Успех",
                    f"PDF документ '{document_type}' успешно сгенерирован!"
                )
                self.load_data()
                self.order_combo.setCurrentIndex(0)
            else:
                QMessageBox.warning(self, "Ошибка", result)

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при создании документа: {str(e)}")

    def delete(self):
        """Delete selected document"""
        if not self.selected_doc_id:
            QMessageBox.warning(self, "Ошибка", "Выберите документ для удаления!")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить этот документ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.service.delete_document(self.selected_doc_id)
                self.load_data()
                QMessageBox.information(self, "Успешно", "Документ удалён!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка удаления документа: {str(e)}")

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

        #formCombo {
            padding: 10px;
            border-radius: 8px;
            background-color: #1e293b;
            border: 1px solid #334155;
            color: white;
            min-height: 35px;
        }

        #formCombo:hover {
            border: 1px solid #475569;
        }

        #documentTable {
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
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            border: none;
            min-width: 150px;
        }

        #btnAdd:hover {
            background-color: #059669;
        }

        #btnDelete {
            background-color: #ef4444;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            border: none;
            min-width: 150px;
        }

        #btnDelete:hover {
            background-color: #dc2626;
        }

        #btnRefresh {
            background-color: #f59e0b;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            border: none;
            min-width: 100px;
        }

        #btnRefresh:hover {
            background-color: #d97706;
        }

        #card {
            background-color: #1e293b;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #334155;
        }

        QComboBox::drop-down {
            border: none;
        }

        QComboBox::down-arrow {
            image: none;
        }
        """