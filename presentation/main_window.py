from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QFrame,
    QSpacerItem,
    QSizePolicy,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem
)

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor

from presentation.clients.client_window import ClientWindow
from presentation.products.product_window import ProductWindow
from presentation.documents.document_window import DocumentWindow
from presentation.orders.orders_window import OrderWindow
from presentation.employees_window import EmployeeWindow

from business.dashboard_service import DashboardService


class MainWindow(QMainWindow):

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.dashboard = DashboardService()

        self.setWindowTitle("Продажы")
        self.resize(1200, 750)

        self.setStyleSheet(self.styles())

        # кнопки для active state
        self.menu_buttons = []

        self.init_ui()

    # ================= UI =================

    def init_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== SIDEBAR =====
        sidebar = QFrame()
        sidebar.setFixedWidth(280)
        sidebar.setObjectName("sidebar")

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(15)
        sidebar_layout.setContentsMargins(20, 25, 20, 25)

        logo = QLabel("📊 Продажы")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setObjectName("logo")
        sidebar_layout.addWidget(logo)

        # Separator line
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFixedHeight(2)
        sidebar_layout.addWidget(separator)

        # ===== MENU BUTTONS =====
        client_btn = self.create_menu_button("👥 Клиенты", self.open_clients)
        product_btn = self.create_menu_button("📦 Товары", self.open_products)
        document_btn = self.create_menu_button("🧾 Документы", self.open_documents)
        order_btn = self.create_menu_button("🛒 Заказы", self.open_orders)
        employee_btn = self.create_menu_button("💼 Сотрудники", self.open_employees)

        self.menu_buttons = [client_btn, product_btn, document_btn, order_btn, employee_btn]

        for btn in self.menu_buttons:
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        sidebar.setLayout(sidebar_layout)

        # ===== CONTENT =====
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea")
        
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(20)

        # HEADER CARD
        header = QFrame()
        header.setObjectName("dashboardHeader")
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(30, 25, 30, 25)

        welcome = QLabel(f"Добро пожаловать")
        welcome.setObjectName("title")

        subtitle = QLabel(f"Система управления продажами")
        subtitle.setObjectName("subtitle")

        header_layout.addWidget(welcome)
        header_layout.addWidget(subtitle)
        header.setLayout(header_layout)
        content_layout.addWidget(header)

        # ===== KEY METRICS =====
        stats = self.dashboard.get_statistics()

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)

        stats_layout.addWidget(self.stat_card("👥 Клиенты", str(stats["clients"]), "#38bdf8"))
        stats_layout.addWidget(self.stat_card("📦 Товары", str(stats["products"]), "#10b981"))
        stats_layout.addWidget(self.stat_card("🛒 Заказы", str(stats["orders"]), "#f59e0b"))
        stats_layout.addWidget(self.stat_card("💰 Доход", f"{int(stats['total']):,.0f} ₽", "#8b5cf6"))

        content_layout.addLayout(stats_layout)

        # ===== DASHBOARD GRID =====
        dashboard_grid = QHBoxLayout()
        dashboard_grid.setSpacing(20)

        # Left column - Recent orders
        left_column = QVBoxLayout()
        left_column.addWidget(self.create_recent_orders_section())
        dashboard_grid.addLayout(left_column, 2)

        # Right column - Quick stats and info
        right_column = QVBoxLayout()
        right_column.addWidget(self.create_quick_stats_section(stats))
        right_column.addWidget(self.create_system_info_section())
        dashboard_grid.addLayout(right_column, 1)

        content_layout.addLayout(dashboard_grid)
        content_layout.addStretch()

        content.setLayout(content_layout)
        scroll.setWidget(content)

        # ===== MAIN =====
        main_layout.addWidget(sidebar)
        main_layout.addWidget(scroll)

        central.setLayout(main_layout)

    # ================= MENU BUTTON =================

    def create_menu_button(self, text, handler):
        btn = QPushButton(text)
        btn.setObjectName("menuButton")
        btn.clicked.connect(lambda: self.set_active(btn, handler))
        return btn

    def set_active(self, button, handler):
        for btn in self.menu_buttons:
            btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        button.setProperty("active", True)
        button.style().unpolish(button)
        button.style().polish(button)

        handler()

    # ================= STAT CARD =================

    def stat_card(self, title, value, color="#38bdf8"):
        card = QFrame()
        card.setObjectName("statCard")
        card.setMinimumHeight(120)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("statTitle")

        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        value_label.setStyleSheet(f"color: {color};")

        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(value_label)

        card.setLayout(layout)

        return card

    def create_recent_orders_section(self):
        section = QFrame()
        section.setObjectName("dashboardSection")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        title = QLabel("📋 Последние заказы")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        orders_container = QWidget()
        orders_layout = QVBoxLayout()
        orders_layout.setSpacing(10)
        orders_layout.setContentsMargins(0, 0, 0, 0)

        try:
            cursor = self.dashboard.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    o.order_id, 
                    c.full_name, 
                    o.total_amount, 
                    o.status, 
                    o.order_date
                FROM Orders o
                LEFT JOIN Clients c ON o.client_id = c.client_id
                ORDER BY o.order_date DESC
                LIMIT 5
            """)
            
            orders = cursor.fetchall()
            
            if orders:
                for order in orders:
                    order_card = self.create_order_card(
                        order['order_id'],
                        order['full_name'] or "Unknown Client",
                        order['total_amount'],
                        order['status'],
                        order['order_date']
                    )
                    orders_layout.addWidget(order_card)
            else:
                empty_label = QLabel("Нет заказов")
                empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                empty_label.setObjectName("emptyState")
                orders_layout.addWidget(empty_label)

        except Exception as e:
            print(f"Error loading orders: {e}")
            error_label = QLabel(f"⚠️ Ошибка загрузки: {str(e)}")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_label.setObjectName("errorState")
            orders_layout.addWidget(error_label)

        orders_layout.addStretch()
        orders_container.setLayout(orders_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(orders_container)
        scroll.setObjectName("ordersScroll")
        scroll.setMaximumHeight(400)
        
        layout.addWidget(scroll)
        section.setLayout(layout)
        return section

    def create_order_card(self, order_id, client_name, amount, status, created_at):
        card = QFrame()
        card.setObjectName("orderCard")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(15)

        # Left - Order ID and client
        left_layout = QVBoxLayout()
        left_layout.setSpacing(5)
        
        order_id_label = QLabel(f"#{order_id}")
        order_id_label.setObjectName("orderID")
        
        client_label = QLabel(client_name)
        client_label.setObjectName("orderClient")
        
        left_layout.addWidget(order_id_label)
        left_layout.addWidget(client_label)
        
        layout.addLayout(left_layout, 1)

        # Middle - Amount
        amount_label = QLabel(f"{int(amount):,.0f} ₽")
        amount_label.setObjectName("orderAmount")
        layout.addWidget(amount_label)

        # Right - Status badge
        status_badge = self.create_status_badge(status)
        layout.addWidget(status_badge)

        card.setLayout(layout)
        return card

    def create_status_badge(self, status):
        badge = QFrame()
        badge.setObjectName("statusBadge")
        
        # Set specific object name based on status for different colors
        status_map = {
            "New": "statusBadgePending",
            "Processing": "statusBadgeProcessing",
            "Completed": "statusBadgeCompleted",
            "Cancelled": "statusBadgeCancelled"
        }
        
        status_text_map = {
            "New": "🆕 Новый",
            "Processing": "⚙️ В обработке",
            "Completed": "✅ Завершён",
            "Cancelled": "❌ Отменён"
        }
        
        badge.setObjectName(status_map.get(status, "statusBadgePending"))
        
        badge_layout = QVBoxLayout()
        badge_layout.setContentsMargins(10, 6, 10, 6)
        badge_layout.setSpacing(0)
        
        status_label = QLabel(status_text_map.get(status, status))
        status_label.setObjectName("statusText")
        
        badge_layout.addWidget(status_label)
        badge.setLayout(badge_layout)
        
        return badge

    def create_quick_stats_section(self, stats):
        section = QFrame()
        section.setObjectName("dashboardSection")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        title = QLabel("📊 Краткая статистика")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        stats_items = [
            ("Среднее значение заказа", f"{int(stats['total'] / max(stats['orders'], 1)):,.0f} ₽", "#06b6d4"),
            ("Товаров в каталоге", str(stats['products']), "#10b981"),
            ("Активных клиентов", str(stats['clients']), "#38bdf8"),
        ]

        for label, value, color in stats_items:
            item_frame = QFrame()
            item_frame.setObjectName("statItem")
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(12, 10, 12, 10)

            label_widget = QLabel(label)
            label_widget.setObjectName("statItemLabel")
            
            value_widget = QLabel(value)
            value_widget.setObjectName("statItemValue")
            value_widget.setStyleSheet(f"color: {color};")

            item_layout.addWidget(label_widget)
            item_layout.addStretch()
            item_layout.addWidget(value_widget)

            item_frame.setLayout(item_layout)
            layout.addWidget(item_frame)

        layout.addStretch()
        section.setLayout(layout)
        return section

    def create_system_info_section(self):
        section = QFrame()
        section.setObjectName("dashboardSection")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)

        title = QLabel("⚙️ Информация системы")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        info_items = [
            ("Текущий пользователь", self.user['full_name']),
            ("Роль", self.user['role'].capitalize()),
            ("Версия системы", "1.0.0"),
            ("Статус БД", "✓ Активна"),
        ]

        for label, value in info_items:
            item_frame = QFrame()
            item_frame.setObjectName("infoItem")
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(12, 8, 12, 8)

            label_widget = QLabel(label)
            label_widget.setObjectName("infoLabel")
            
            value_widget = QLabel(value)
            value_widget.setObjectName("infoValue")

            item_layout.addWidget(label_widget)
            item_layout.addStretch()
            item_layout.addWidget(value_widget)

            item_frame.setLayout(item_layout)
            layout.addWidget(item_frame)

        layout.addStretch()
        section.setLayout(layout)
        return section

    # ================= WINDOWS =================

    def open_clients(self):
        self.client_window = ClientWindow()
        self.client_window.show()

    def open_products(self):
        self.product_window = ProductWindow()
        self.product_window.show()

    def open_documents(self):
        self.document_window = DocumentWindow()
        self.document_window.show()

    def open_orders(self):
        self.order_window = OrderWindow()
        self.order_window.show()

    def open_employees(self):
        self.employee_window = EmployeeWindow()
        self.employee_window.show()

    # ================= STYLES =================

    def styles(self):
        return """
        QWidget {
            background-color: #0a0f1f;
            color: white;
            font-size: 14px;
        }

        QFrame {
            background-color: #0f1729;
            border-radius: 12px;
        }

        #scrollArea {
            border: none;
        }

        #ordersScroll {
            border: none;
        }

        QScrollBar:vertical {
            background-color: #0a0f1f;
            width: 10px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical {
            background-color: #475569;
            border-radius: 5px;
            min-height: 20px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #64748b;
        }

        #sidebar {
            background: linear-gradient(180deg, #0d1728 0%, #0a0f1f 100%);
            border-right: 1px solid #1e293b;
        }

        #logo {
            font-size: 28px;
            font-weight: bold;
            color: #0ea5e9;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        #separator {
            background: linear-gradient(90deg, transparent 0%, #334155 50%, transparent 100%);
        }

        #title {
            font-size: 28px;
            font-weight: bold;
            color: #f1f5f9;
            letter-spacing: -0.5px;
        }

        #subtitle {
            color: #94a3b8;
            font-size: 14px;
            font-weight: 500;
        }

        #dashboardHeader {
            background: linear-gradient(135deg, #1a2332 0%, #0f1728 100%);
            border: 1px solid #334155;
            border-radius: 18px;
            min-height: 110px;
        }

        #menuButton {
            background-color: #1a2332;
            border-radius: 12px;
            padding: 14px 16px;
            text-align: left;
            font-size: 14px;
            font-weight: 600;
            border: 2px solid transparent;
            color: #cbd5e1;
            margin: 2px 0px;
        }

        #menuButton:hover {
            background-color: #273449;
            border: 2px solid #0ea5e9;
            color: #f1f5f9;
        }

        QPushButton[active="true"] {
            background: linear-gradient(135deg, #273449 0%, #1a2f45 100%);
            border: 2px solid #0ea5e9;
            color: #f1f5f9;
        }

        #statCard {
            background: linear-gradient(135deg, #1a2f45 0%, #152238 100%);
            border-radius: 14px;
            border: 1px solid #334155;
            min-height: 130px;
            padding: 0px;
        }

        #statCard:hover {
            border: 1px solid #0ea5e9;
            background: linear-gradient(135deg, #1a2f45 0%, #1a3a52 100%);
            box-shadow: 0 8px 24px rgba(14, 165, 233, 0.15);
        }

        #statTitle {
            color: #cbd5e1;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        #statValue {
            font-size: 36px;
            font-weight: bold;
            color: #0ea5e9;
        }

        #dashboardSection {
            background: linear-gradient(135deg, #1a2f45 0%, #152238 100%);
            border: 1px solid #334155;
            border-radius: 14px;
            min-height: 280px;
        }

        #dashboardSection:hover {
            border: 1px solid #475569;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }

        #sectionTitle {
            font-size: 20px;
            font-weight: bold;
            color: #f1f5f9;
            letter-spacing: -0.3px;
        }

        #orderCard {
            background: linear-gradient(135deg, #1a2f45 0%, #152238 100%);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 0px;
            min-height: 85px;
        }

        #orderCard:hover {
            border: 1px solid #0ea5e9;
            background: linear-gradient(135deg, #1a3a52 0%, #1a2f45 100%);
            box-shadow: 0 6px 20px rgba(14, 165, 233, 0.12);
        }

        #orderID {
            font-size: 15px;
            font-weight: bold;
            color: #0ea5e9;
        }

        #orderClient {
            font-size: 13px;
            color: #cbd5e1;
        }

        #orderAmount {
            font-size: 16px;
            font-weight: bold;
            color: #10b981;
            min-width: 120px;
            text-align: right;
        }

        #statusBadge {
            background-color: transparent;
            border: none;
            border-radius: 6px;
            padding: 0px;
            min-width: 110px;
        }

        #statusBadgePending {
            background-color: #b45309;
            border: 1px solid #d97706;
        }

        #statusBadgeProcessing {
            background-color: #0369a1;
            border: 1px solid #0ea5e9;
        }

        #statusBadgeCompleted {
            background-color: #047857;
            border: 1px solid #10b981;
        }

        #statusBadgeCancelled {
            background-color: #7f1d1d;
            border: 1px solid #ef4444;
        }

        #statusText {
            font-size: 12px;
            font-weight: 600;
            color: white;
            text-align: center;
        }

        #emptyState {
            color: #94a3b8;
            font-size: 15px;
            padding: 40px;
        }

        #errorState {
            color: #ef4444;
            font-size: 14px;
            padding: 40px;
        }

        #dashboardTable {
            background-color: #0f172a;
            border: none;
            gridline-color: #1e293b;
            border-radius: 8px;
        }

        QTableWidget::item {
            padding: 8px 4px;
            color: #cbd5e1;
        }

        QTableWidget::item:selected {
            background-color: #334155;
        }

        QHeaderView::section {
            background-color: #1e293b;
            color: #94a3b8;
            padding: 8px;
            border: none;
            font-weight: bold;
            font-size: 13px;
        }

        #statItem {
            background-color: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 0px;
        }

        #statItem:hover {
            border: 1px solid #475569;
        }

        #statItemLabel {
            color: #94a3b8;
            font-size: 13px;
        }

        #statItemValue {
            font-weight: bold;
            font-size: 14px;
        }

        #infoItem {
            background-color: #0f172a;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 0px;
        }

        #infoItem:hover {
            border: 1px solid #38bdf8;
        }

        #infoLabel {
            color: #94a3b8;
            font-size: 13px;
        }

        #infoValue {
            color: #cbd5e1;
            font-weight: 600;
        }
        """