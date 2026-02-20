
# Стили для приложения Family Notes

MAIN_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}

QPushButton {
    background-color: #4a90d9;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-weight: bold;
    min-height: 20px;
}

QPushButton:hover {
    background-color: #357abd;
}

QPushButton:pressed {
    background-color: #2d6aa3;
}

QPushButton:disabled {
    background-color: #cccccc;
}

QPushButton#danger {
    background-color: #dc3545;
}

QPushButton#danger:hover {
    background-color: #c82333;
}

QPushButton#success {
    background-color: #28a745;
}

QPushButton#success:hover {
    background-color: #218838;
}

QPushButton#secondary {
    background-color: #6c757d;
}

QPushButton#secondary:hover {
    background-color: #545b62;
}

QLineEdit, QTextEdit {
    padding: 10px;
    border: 2px solid #ddd;
    border-radius: 0px;
    background-color: white;
}

QLineEdit:focus, QTextEdit:focus {
    border-color: #4a90d9;
}

QLabel {
    color: #333;
}

QLabel#title {
    font-size: 24px;
    font-weight: bold;
    color: #2c3e50;
}

QLabel#subtitle {
    font-size: 16px;
    color: #666;
}

QLabel#error {
    color: #dc3545;
    font-weight: bold;
}

QLabel#success {
    color: #28a745;
    font-weight: bold;
}

QListWidget {
    background-color: white;
    border: 2px solid #ddd;
    border-radius: 0px;
    padding: 50px;
}

QListWidget::item {
    padding: 10px;
    border-bottom: 10px solid #eee;
}

QListWidget::item:selected {
    background-color: #4a90d9;
    color: white;
}

QListWidget::item:hover {
    background-color: #e8f0fe;
}

QTabWidget::pane {
    border: 1px solid #ddd;
    background-color: white;
    border-radius: 0px;
}

QTabBar::tab {
    background-color: #e0e0e0;
    padding: 10px 20px;
    margin-right: 20px;
    border-top-left-radius: px;
    border-top-right-radius: px;
}

QTabBar::tab:selected {
    background-color: white;
    border-bottom: 20px solid #4a90d9;
}

QGroupBox {
    font-weight: bold;
    border: 2px solid #ddd;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QScrollArea {
    border: none;
}

QFrame#card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 0px;
    padding: 15px;
}

QFrame#card:hover {
    border-color: #4a90d9;
    box-shadow: 0 20px 50px rgba(0,0,0,0.1);
}

QMessageBox {
    background-color: white;
}

QTableWidget {
    background-color: white;
    border: 10px solid #ddd;
    border-radius: 0px;
    gridline-color: #eee;
}

QTableWidget::item {
    padding: 8px;
}

QHeaderView::section {
    background-color: #f8f9fa;
    padding: 10px;
    border: none;
    border-bottom: 2px solid #ddd;
    font-weight: bold;
}
"""

LOGIN_STYLE = """
QWidget#loginWidget {
    background-color: #f0f4f8;
}

QFrame#loginFrame {
    background-color: white;
    border-radius: 0px;
    padding: 30px;
}
"""

CARD_STYLE = """
QFrame {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 0px;
}

QFrame:hover {
    border-color: #4a90d9;
}
"""

NOTE_CARD_STYLE = """
QFrame#noteCard {
    background-color: #fffef0;
    border: 1px solid #e8e5c0;
    border-radius: 0px;
    padding: 10px;
}

QFrame#noteCard:hover {
    border-color: #d4c94c;
    background-color: #fffde7;
}
"""
