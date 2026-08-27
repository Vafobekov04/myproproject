import json
import os
from pathlib import Path


class ThemeManager:
    """Управление темами приложения (светлая/темная)"""
    
    THEMES = {
        "light": {
            "bg_primary": "#FFFFFF",
            "bg_secondary": "#F5F5F5",
            "text_primary": "#1A1A1A",
            "text_secondary": "#666666",
            "border": "#E0E0E0",
            "accent": "#0066CC",
            "accent_hover": "#0052A3",
            "success": "#28A745",
            "error": "#DC3545",
            "warning": "#FFC107",
            "sidebar_bg": "#F8F9FA",
            "button_bg": "#E9ECEF",
            "button_hover": "#DEE2E6",
            "input_bg": "#FFFFFF",
            "input_border": "#CED4DA",
        },
        "dark": {
            "bg_primary": "#1E1E1E",
            "bg_secondary": "#2D2D2D",
            "text_primary": "#E0E0E0",
            "text_secondary": "#999999",
            "border": "#404040",
            "accent": "#4A9EFF",
            "accent_hover": "#6BB3FF",
            "success": "#4CAF50",
            "error": "#FF5252",
            "warning": "#FFB74D",
            "sidebar_bg": "#252525",
            "button_bg": "#3A3A3A",
            "button_hover": "#454545",
            "input_bg": "#2D2D2D",
            "input_border": "#404040",
        }
    }
    
    CONFIG_PATH = Path.home() / ".sales_system" / "theme.json"
    
    def __init__(self):
        self.current_theme = self._load_theme()
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Создать директорию конфига если её нет"""
        self.CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_theme(self) -> str:
        """Загрузить сохраненную тему или вернуть по умолчанию"""
        try:
            if self.CONFIG_PATH.exists():
                with open(self.CONFIG_PATH, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    theme = config.get("theme", "light")
                    if theme in self.THEMES:
                        return theme
        except Exception:
            pass
        return "light"
    
    def _save_theme(self, theme: str):
        """Сохранить выбранную тему"""
        try:
            self._ensure_config_dir()
            with open(self.CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump({"theme": theme}, f)
        except Exception:
            pass
    
    def set_theme(self, theme_name: str) -> bool:
        """Переключить тему"""
        if theme_name not in self.THEMES:
            return False
        self.current_theme = theme_name
        self._save_theme(theme_name)
        return True
    
    def get_theme(self) -> str:
        """Получить текущую тему"""
        return self.current_theme
    
    def get_colors(self) -> dict:
        """Получить цветовую схему текущей темы"""
        return self.THEMES[self.current_theme].copy()
    
    def get_stylesheet(self) -> str:
        """Получить CSS стили для текущей темы"""
        colors = self.get_colors()
        
        stylesheet = f"""
        QMainWindow {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
        }}
        
        QWidget {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
        }}
        
        #sidebar {{
            background: qlineargradient(x1:0, y1:0, x1:0, y2:1, stop:0 {colors['sidebar_bg']}, stop:1 {colors['bg_secondary']});
            border-right: 1px solid {colors['border']};
        }}
        
        #logo {{
            font-size: 18px;
            font-weight: bold;
            background: qlineargradient(x1:0, y1:0, x1:1, y2:0, stop:0 {colors['accent']}, stop:1 #10b981);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 25px;
        }}
        
        #title {{
            font-size: 16px;
            font-weight: bold;
            color: {colors['accent']};
            margin-bottom: 20px;
        }}
        
        #menuSeparator {{
            height: 1px;
            background-color: {colors['border']};
            margin: 10px 0;
        }}
        
        QPushButton {{
            background-color: {colors['button_bg']};
            color: {colors['text_primary']};
            border: 1px solid {colors['border']};
            border-radius: 4px;
            padding: 8px 12px;
            font-size: 13px;
        }}
        
        QPushButton:hover {{
            background-color: {colors['button_hover']};
        }}
        
        QPushButton:pressed {{
            background-color: {colors['accent']};
            color: white;
        }}
        
        QPushButton#menuBtn {{
            text-align: left;
            padding: 12px 15px;
            border: none;
            border-radius: 8px;
            background-color: transparent;
            font-size: 14px;
            font-weight: 500;
            color: {colors['text_secondary']};
            margin: 4px 0px;
        }}
        
        QPushButton#menuBtn:hover {{
            background-color: {colors['button_bg']};
            color: {colors['text_primary']};
        }}
        
        QPushButton#menuBtn:pressed,
        QPushButton#menuBtn.active {{
            background: qlineargradient(x1:0, y1:0, x1:1, y2:0, stop:0 {colors['accent']}, stop:1 {colors['accent_hover']});
            color: white;
            font-weight: 600;
        }}
        
        QPushButton#themeBtn {{
            background-color: {colors['accent']};
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
        }}
        
        QPushButton#themeBtn:hover {{
            background-color: {colors['accent_hover']};
        }}
        
        QLabel {{
            color: {colors['text_primary']};
        }}
        
        QLabel#dashboardHeader {{
            color: {colors['text_primary']};
        }}
        
        QFrame {{
            background-color: {colors['bg_secondary']};
            border: 1px solid {colors['border']};
            border-radius: 12px;
        }}
        
        QFrame#dashboardHeader {{
            background: qlineargradient(x1:0, y1:0, x1:1, y2:1, stop:0 {colors['accent']}, stop:1 {colors['accent_hover']});
            border: none;
            padding: 30px;
            border-radius: 18px;
        }}
        
        QFrame#dashboardHeader QLabel {{
            color: white;
        }}
        
        QFrame#statCard {{
            background-color: {colors['bg_secondary']};
            border: 2px solid {colors['border']};
            border-radius: 14px;
            padding: 20px;
        }}
        
        QFrame#statCard:hover {{
            border: 3px solid {colors['accent']};
            background-color: {colors['bg_secondary']};
        }}
        
        QLineEdit, QTextEdit {{
            background-color: {colors['input_bg']};
            color: {colors['text_primary']};
            border: 1px solid {colors['input_border']};
            border-radius: 4px;
            padding: 8px;
            selection-background-color: {colors['accent']};
        }}
        
        QLineEdit:focus, QTextEdit:focus {{
            border: 2px solid {colors['accent']};
        }}
        
        QTableWidget {{
            background-color: {colors['bg_primary']};
            alternate-background-color: {colors['bg_secondary']};
            gridline-color: {colors['border']};
            color: {colors['text_primary']};
        }}
        
        QTableWidget::item {{
            padding: 5px;
        }}
        
        QTableWidget::item:selected {{
            background-color: {colors['accent']};
            color: white;
        }}
        
        QHeaderView::section {{
            background-color: {colors['sidebar_bg']};
            color: {colors['text_primary']};
            padding: 5px;
            border: none;
            border-right: 1px solid {colors['border']};
        }}
        
        QComboBox {{
            background-color: {colors['input_bg']};
            color: {colors['text_primary']};
            border: 1px solid {colors['input_border']};
            border-radius: 4px;
            padding: 5px;
        }}
        
        QComboBox:focus {{
            border: 2px solid {colors['accent']};
        }}
        
        QComboBox::drop-down {{
            border: none;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            width: 0px;
        }}
        
        QSpinBox, QDoubleSpinBox {{
            background-color: {colors['input_bg']};
            color: {colors['text_primary']};
            border: 1px solid {colors['input_border']};
            border-radius: 4px;
            padding: 5px;
        }}
        
        QSpinBox:focus, QDoubleSpinBox:focus {{
            border: 2px solid {colors['accent']};
        }}
        
        QDateEdit {{
            background-color: {colors['input_bg']};
            color: {colors['text_primary']};
            border: 1px solid {colors['input_border']};
            border-radius: 4px;
            padding: 5px;
        }}
        
        QDateEdit:focus {{
            border: 2px solid {colors['accent']};
        }}
        
        QScrollArea {{
            background-color: {colors['bg_primary']};
            border: none;
        }}
        
        QScrollBar:vertical {{
            background-color: {colors['bg_secondary']};
            width: 12px;
            border: none;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors['border']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['accent']};
        }}
        
        QScrollBar:horizontal {{
            background-color: {colors['bg_secondary']};
            height: 12px;
            border: none;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {colors['border']};
            border-radius: 6px;
            min-width: 20px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {colors['accent']};
        }}
        
        QDialog {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
        }}
        
        QMenuBar {{
            background-color: {colors['sidebar_bg']};
            color: {colors['text_primary']};
            border-bottom: 1px solid {colors['border']};
        }}
        
        QMenuBar::item:selected {{
            background-color: {colors['button_hover']};
        }}
        
        QMenu {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_primary']};
            border: 1px solid {colors['border']};
        }}
        
        QMenu::item:selected {{
            background-color: {colors['accent']};
            color: white;
        }}
        
        QMessageBox {{
            background-color: {colors['bg_primary']};
        }}
        
        QMessageBox QLabel {{
            color: {colors['text_primary']};
        }}
        
        #dashboardSection {{
            background-color: {colors['bg_secondary']};
            border: 2px solid {colors['border']};
            border-radius: 14px;
            min-height: 250px;
            padding: 0px;
        }}
        
        #dashboardSection:hover {{
            border: 3px solid {colors['accent']};
            background-color: {colors['bg_secondary']};
        }}
        
        #orderCard {{
            background-color: {colors['bg_secondary']};
            border: 2px solid {colors['border']};
            border-radius: 10px;
            padding: 0px;
            margin: 5px 0px;
        }}
        
        #orderCard:hover {{
            border: 2px solid {colors['accent']};
            background-color: {colors['bg_secondary']};
        }}
        
        #orderID {{
            font-size: 15px;
            font-weight: bold;
            color: {colors['accent']};
        }}
        
        #orderClient {{
            font-size: 13px;
            color: {colors['text_secondary']};
        }}
        
        #orderAmount {{
            font-size: 16px;
            font-weight: bold;
            color: #10b981;
            min-width: 120px;
            text-align: right;
        }}
        
        #statItem {{
            background-color: {colors['bg_primary']};
            border: 2px solid {colors['border']};
            border-radius: 10px;
            padding: 0px;
            margin: 3px 0px;
        }}
        
        #statItem:hover {{
            border: 2px solid {colors['accent']};
        }}
        
        #infoItem {{
            background-color: {colors['bg_primary']};
            border: 2px solid {colors['border']};
            border-radius: 10px;
            padding: 0px;
            margin: 3px 0px;
        }}
        
        #infoItem:hover {{
            border: 2px solid {colors['accent']};
        }}
        
        #sectionTitle {{
            font-size: 18px;
            font-weight: bold;
            color: {colors['accent']};
            margin-bottom: 8px;
        }}
        
        #title {{
            font-size: 28px;
            font-weight: bold;
            color: {colors['accent']};
            margin-bottom: 15px;
        }}
        
        #subtitle {{
            font-size: 14px;
            color: {colors['text_secondary']};
        }}
        
        #statTitle {{
            color: {colors['text_secondary']};
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        #statValue {{
            font-size: 42px;
            font-weight: bold;
            color: {colors['accent']};
            text-align: center;
        }}
        
        #statItemLabel {{
            color: {colors['text_secondary']};
            font-size: 13px;
            font-weight: 500;
        }}
        
        #statItemValue {{
            font-weight: bold;
            font-size: 15px;
        }}
        
        #infoLabel {{
            color: {colors['text_secondary']};
            font-size: 13px;
            font-weight: 500;
        }}
        
        #infoValue {{
            color: {colors['text_primary']};
            font-weight: 600;
            font-size: 13px;
        }}
        
        #statusBadge {{
            background-color: {colors['bg_secondary']};
            border: 2px solid {colors['border']};
            border-radius: 8px;
            padding: 8px 12px;
        }}
        
        #statusBadgePending {{
            background-color: rgba(255, 193, 7, 0.1);
            border: 2px solid #FFC107;
        }}
        
        #statusBadgeProcessing {{
            background-color: rgba(33, 150, 243, 0.1);
            border: 2px solid #2196F3;
        }}
        
        #statusBadgeCompleted {{
            background-color: rgba(76, 175, 80, 0.1);
            border: 2px solid #4CAF50;
        }}
        
        #statusBadgeCancelled {{
            background-color: rgba(244, 67, 54, 0.1);
            border: 2px solid #F44336;
        }}
        
        #statusText {{
            font-weight: bold;
            font-size: 11px;
        }}
        
        #statusBadgePending #statusText {{
            color: #F57F17;
        }}
        
        #statusBadgeProcessing #statusText {{
            color: #1565C0;
        }}
        
        #statusBadgeCompleted #statusText {{
            color: #2E7D32;
        }}
        
        #statusBadgeCancelled #statusText {{
            color: #C62828;
        }}
        """
        
        return stylesheet
