"""
Пример: Как добавить поддержку темы в ваше окно

Этот файл показывает, как интегрировать ThemeManager в любое окно приложения
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from utils.theme_manager import ThemeManager


class ExampleWindowWithTheme(QMainWindow):
    """Пример окна с поддержкой темы"""
    
    def __init__(self):
        super().__init__()
        
        # 1. Создайте экземпляр ThemeManager
        self.theme_manager = ThemeManager()
        
        # 2. Установите стили из темы
        self.setStyleSheet(self.theme_manager.get_stylesheet())
        
        # 3. Создайте интерфейс
        self.setup_ui()
        
        self.setWindowTitle("Example Window with Theme Support")
        self.resize(500, 400)
    
    def setup_ui(self):
        """Создать интерфейс"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout()
        
        # Текущая тема
        theme_label = QLabel(f"Текущая тема: {self.theme_manager.get_theme()}")
        theme_label.setObjectName("title")
        layout.addWidget(theme_label)
        
        # Кнопка для переключения темы
        toggle_btn = QPushButton("Переключить тему")
        toggle_btn.clicked.connect(self.on_toggle_theme)
        layout.addWidget(toggle_btn)
        
        # Информация о цветах
        colors = self.theme_manager.get_colors()
        info = QLabel(f"Цвет акцента: {colors['accent']}")
        layout.addWidget(info)
        
        layout.addStretch()
        central.setLayout(layout)
    
    def on_toggle_theme(self):
        """Переключить тему"""
        current = self.theme_manager.get_theme()
        new_theme = "dark" if current == "light" else "light"
        
        # Установить новую тему
        self.theme_manager.set_theme(new_theme)
        
        # Обновить стили
        self.setStyleSheet(self.theme_manager.get_stylesheet())
        
        # Обновить интерфейс
        for widget in self.findChildren(QLabel):
            if "Текущая тема" in widget.text():
                widget.setText(f"Текущая тема: {new_theme}")


# ============================================================================
# БЫСТРЫЙ СТАРТ
# ============================================================================
# 
# Минимум кода для добавления поддержки темы:
#
# 1. Импортируйте ThemeManager:
#    from utils.theme_manager import ThemeManager
#
# 2. В вашем __init__:
#    self.theme_manager = ThemeManager()
#    self.setStyleSheet(self.theme_manager.get_stylesheet())
#
# 3. Для переключения темы:
#    def toggle_theme(self):
#        current = self.theme_manager.get_theme()
#        new_theme = "dark" if current == "light" else "light"
#        self.theme_manager.set_theme(new_theme)
#        self.setStyleSheet(self.theme_manager.get_stylesheet())
#
# ============================================================================
# ПОЛЕЗНЫЕ МЕТОДЫ
# ============================================================================
#
# theme_manager.get_theme()        # Получить "light" или "dark"
# theme_manager.set_theme("dark")  # Установить тему
# theme_manager.get_colors()       # Получить словарь цветов
# theme_manager.get_stylesheet()   # Получить CSS стили
#
# ============================================================================
# ПАЛИТРА ЦВЕТОВ
# ============================================================================
#
# colors = theme_manager.get_colors()
#
# Доступные ключи:
# - bg_primary         # Основной цвет фона
# - bg_secondary       # Вторичный цвет фона
# - text_primary       # Основной цвет текста
# - text_secondary     # Вторичный цвет текста
# - border             # Цвет границ
# - accent             # Цвет акцента
# - accent_hover       # Цвет акцента при наведении
# - success            # Цвет успеха
# - error              # Цвет ошибки
# - warning            # Цвет предупреждения
# - sidebar_bg         # Цвет фона боковой панели
# - button_bg          # Цвет фона кнопки
# - button_hover       # Цвет фона кнопки при наведении
# - input_bg           # Цвет фона поля ввода
# - input_border       # Цвет границы поля ввода
#
# ============================================================================


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = ExampleWindowWithTheme()
    window.show()
    sys.exit(app.exec())
