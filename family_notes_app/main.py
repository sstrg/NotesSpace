
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from database import Database
from pages import LoginPage, RegisterPage, HomePage, SpacePage
from styles import MAIN_STYLE


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.current_user = None
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Семейные заметки")
        self.setMinimumSize(900, 700)
        self.setStyleSheet(MAIN_STYLE)
        
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - 900) // 2
        y = (screen.height() - 700) // 2
        self.setGeometry(x, y, 900, 700)
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        self.login_page = LoginPage(self.db)
        self.login_page.login_success.connect(self.on_login_success)
        self.login_page.switch_to_register.connect(self.show_register_page)
        self.stack.addWidget(self.login_page)
        
        self.register_page = RegisterPage(self.db)
        self.register_page.register_success.connect(self.show_login_page)
        self.register_page.switch_to_login.connect(self.show_login_page)
        self.stack.addWidget(self.register_page)
        
        self.stack.setCurrentWidget(self.login_page)
    
    def show_login_page(self):
        self.stack.setCurrentWidget(self.login_page)
    
    def show_register_page(self):
        self.stack.setCurrentWidget(self.register_page)
    
    def on_login_success(self, user: dict):
        self.current_user = user
        self.show_home_page()
    
    def show_home_page(self):
        for i in range(self.stack.count()):
            widget = self.stack.widget(i)
            if isinstance(widget, HomePage):
                self.stack.removeWidget(widget)
                widget.deleteLater()
        
        self.home_page = HomePage(self.db, self.current_user)
        self.home_page.space_selected.connect(self.on_space_selected)
        self.home_page.logout_requested.connect(self.logout)
        self.stack.addWidget(self.home_page)
        self.stack.setCurrentWidget(self.home_page)
    
    def on_space_selected(self, space: dict):
        space_page = SpacePage(self.db, self.current_user, space)
        space_page.back_requested.connect(self.show_home_page)
        self.stack.addWidget(space_page)
        self.stack.setCurrentWidget(space_page)
    
    def logout(self):
        self.current_user = None
        self.login_page.clear_form()
        self.stack.setCurrentWidget(self.login_page)
    
    def closeEvent(self, event):
        self.db.close()
        event.accept()


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Family Notes")
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
