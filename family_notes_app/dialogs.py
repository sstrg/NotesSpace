
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QPushButton, QMessageBox,
                             QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
import qrcode
from io import BytesIO


class CreateSpaceDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Создать пространство")
        self.setFixedSize(800, 600)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Создать новое пространство")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        layout.addWidget(QLabel("Название:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название пространства")
        layout.addWidget(self.name_input)
        
        layout.addWidget(QLabel("Описание:"))
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Введите описание (необязательно)")
        self.description_input.setFixedHeight(150)
        layout.addWidget(self.description_input)
        
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Отмена")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        create_btn = QPushButton("Создать")
        create_btn.setObjectName("success")
        create_btn.clicked.connect(self.accept)
        btn_layout.addWidget(create_btn)
        
        layout.addLayout(btn_layout)
    
    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "description": self.description_input.toPlainText().strip()
        }


class JoinSpaceDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Присоединиться к пространству")
        self.setFixedSize(350, 180)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Присоединиться по коду")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        layout.addWidget(QLabel("Код приглашения:"))
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Введите 8-символьный код")
        self.code_input.setMaxLength(8)
        self.code_input.setFixedHeight(40)
        layout.addWidget(self.code_input)
        
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Отмена")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        join_btn = QPushButton("Присоединиться")
        join_btn.setObjectName("success")
        join_btn.clicked.connect(self.accept)
        btn_layout.addWidget(join_btn)
        
        layout.addLayout(btn_layout)
    
    def get_code(self):
        return self.code_input.text().strip().upper()


class InviteCodeDialog(QDialog):

    def __init__(self, space_name: str, invite_code: str, parent=None):
        super().__init__(parent)
        self.space_name = space_name
        self.invite_code = invite_code
        self.setWindowTitle("Код приглашения")
        self.setFixedSize(800, 600)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel(f"Пригласить в «{self.space_name}»")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setWordWrap(True)
        layout.addWidget(title)
        
        code_frame = QFrame()
        code_frame.setStyleSheet("""
            QFrame {
                background-color: #f0f4f8;
                border: 2px dashed #4a90d9;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        code_layout = QVBoxLayout(code_frame)
        
        code_label = QLabel("Код приглашения:")
        code_label.setStyleSheet("border: none;")
        code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        code_layout.addWidget(code_label)
        
        code_value = QLabel(self.invite_code)
        code_value.setFont(QFont("Consolas", 24, QFont.Weight.Bold))
        code_value.setStyleSheet("color: #4a90d9; border: none;")
        code_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        code_value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        code_layout.addWidget(code_value)
        
        layout.addWidget(code_frame)
        
        qr_label = QLabel("Или отсканируйте QR-код:")
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(qr_label)
        
        qr_image = self.generate_qr_code()
        qr_display = QLabel()
        qr_display.setPixmap(qr_image)
        qr_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(qr_display)
        
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def generate_qr_code(self) -> QPixmap:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=2,
        )
        qr.add_data(f"FAMILYNOTES:{self.invite_code}")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue())
        
        return pixmap


class NoteDialog(QDialog):

    def __init__(self, note_data: dict = None, parent=None):
        super().__init__(parent)
        self.note_data = note_data
        self.setWindowTitle("Редактировать заметку" if note_data else "Новая заметка")
        self.setFixedSize(500, 400)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Редактировать заметку" if self.note_data else "Создать заметку")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        layout.addWidget(QLabel("Заголовок:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Введите заголовок заметки")
        if self.note_data:
            self.title_input.setText(self.note_data.get("title", ""))
        layout.addWidget(self.title_input)
        
        layout.addWidget(QLabel("Содержимое:"))
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("Введите текст заметки...")
        if self.note_data:
            self.content_input.setText(self.note_data.get("content", ""))
        layout.addWidget(self.content_input)
        
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Отмена")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Сохранить" if self.note_data else "Создать")
        save_btn.setObjectName("success")
        save_btn.clicked.connect(self.accept)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
    
    def get_data(self):
        return {
            "title": self.title_input.text().strip(),
            "content": self.content_input.toPlainText().strip()
        }


class ConfirmDialog(QDialog):

    def __init__(self, title: str, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(350, 150)
        self.setup_ui(title, message)
    
    def setup_ui(self, title: str, message: str):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg_label)
        
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Отмена")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        confirm_btn = QPushButton("Подтвердить")
        confirm_btn.setObjectName("danger")
        confirm_btn.clicked.connect(self.accept)
        btn_layout.addWidget(confirm_btn)
        
        layout.addLayout(btn_layout)
