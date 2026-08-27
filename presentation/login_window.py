from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QMessageBox
)

from business.auth_service import AuthService
from presentation.main_window import MainWindow


class LoginWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.auth_service = AuthService()

        self.setWindowTitle("Авторизация")
        self.resize(400, 250)

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        title = QLabel(
            "Система продаж"
        )

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText(
            "Логин"
        )

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(
            "Пароль"
        )

        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        button = QPushButton(
            "Войти"
        )

        button.clicked.connect(
            self.handle_login
        )

        layout.addWidget(title)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)
        layout.addWidget(button)

        self.setLayout(layout)

    def handle_login(self):

        login = self.login_input.text()
        password = self.password_input.text()

        try:

            user, message = self.auth_service.login(
                login,
                password
            )

            if user:

                self.main_window = MainWindow(user)

                self.main_window.show()

                self.hide()

            else:

                QMessageBox.warning(
                    self,
                    "Ошибка",
                    message
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Ошибка",
                str(e)
            )

            print(e)