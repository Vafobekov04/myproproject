import sys
from PyQt6.QtWidgets import QApplication
from presentation.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # заглушка пользователя (чтобы обойти авторизацию)
    


    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()  
    
    
    
    
    