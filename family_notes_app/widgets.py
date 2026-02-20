
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QSizePolicy)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont


class SpaceCard(QFrame):
    clicked = pyqtSignal(dict)
    
    def __init__(self, space_data: dict, is_owner: bool = False):
        super().__init__()
        self.space_data = space_data
        self.is_owner = is_owner
        self.setup_ui()
    
    def setup_ui(self):
        self.setObjectName("card")
        self.setStyleSheet("""
            QFrame#card {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
            }
            QFrame#card:hover {
                border-color: #4a90d9;
            }
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(120)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title_layout = QHBoxLayout()
        title = QLabel(self.space_data["name"])
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; border: none;")
        title_layout.addWidget(title)
        
        if self.is_owner:
            owner_badge = QLabel("👑 Владелец")
            owner_badge.setStyleSheet("""
                background-color: #ffd700;
                color: #333;
                padding: 3px 8px;
                border-radius: 10px;
                font-size: 11px;
                border: none;
            """)
            title_layout.addWidget(owner_badge)
        
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        if self.space_data.get("description"):
            desc = QLabel(self.space_data["description"][:100] + "..." 
                         if len(self.space_data.get("description", "")) > 100 
                         else self.space_data.get("description", ""))
            desc.setStyleSheet("color: #666; border: none;")
            desc.setWordWrap(True)
            layout.addWidget(desc)
        
        info_layout = QHBoxLayout()
        owner_label = QLabel(f"👤 {self.space_data.get('owner_name', 'Неизвестно')}")
        owner_label.setStyleSheet("color: #888; font-size: 12px; border: none;")
        info_layout.addWidget(owner_label)
        
        info_layout.addStretch()
        
        code_label = QLabel(f"🔗 {self.space_data['invite_code']}")
        code_label.setStyleSheet("color: #4a90d9; font-size: 12px; border: none;")
        info_layout.addWidget(code_label)
        
        layout.addLayout(info_layout)
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.space_data)


class NoteCard(QFrame):
    clicked = pyqtSignal(dict)
    edit_requested = pyqtSignal(dict)
    delete_requested = pyqtSignal(dict)
    
    def __init__(self, note_data: dict):
        super().__init__()
        self.note_data = note_data
        self.setup_ui()
    
    def setup_ui(self):
        self.setObjectName("noteCard")
        self.setStyleSheet("""
            QFrame#noteCard {
                background-color: #fffef0;
                border: 2px solid #e8e5c0;
                border-radius: 8px;
            }
            QFrame#noteCard:hover {
                border-color: #d4c94c;
                background-color: #fffde7;
            }
        """)
        self.setMinimumHeight(100)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        
        header_layout = QHBoxLayout()
        
        title = QLabel(self.note_data["title"])
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #333; border: none; background: transparent;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        edit_btn = QPushButton("✏️")
        edit_btn.setFixedSize(60, 60)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-radius: 15px;
            }
        """)
        edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.note_data))
        header_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(60, 60)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ffcccc;
                border-radius: 15px;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.note_data))
        header_layout.addWidget(delete_btn)
        
        layout.addLayout(header_layout)
        
        content = QLabel(self.note_data["content"][:200] + "..."
                        if len(self.note_data.get("content", "")) > 200 
                        else self.note_data.get("content", ""))
        content.setStyleSheet("color: #555; border: none; background: transparent;")
        content.setWordWrap(True)
        layout.addWidget(content)
        
        meta_layout = QHBoxLayout()
        
        author = QLabel(f"✍️ {self.note_data['author_name']}")
        author.setStyleSheet("color: #888; font-size: 11px; border: none; background: transparent;")
        meta_layout.addWidget(author)
        
        meta_layout.addStretch()
        
        date = QLabel(f"📅 {self.note_data['updated_at'][:16] if self.note_data.get('updated_at') else ''}")
        date.setStyleSheet("color: #888; font-size: 11px; border: none; background: transparent;")
        meta_layout.addWidget(date)
        
        layout.addLayout(meta_layout)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.note_data)


class MemberCard(QFrame):
    remove_requested = pyqtSignal(dict)
    
    def __init__(self, member_data: dict, can_remove: bool = False):
        super().__init__()
        self.member_data = member_data
        self.can_remove = can_remove
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.setFixedHeight(120)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        icon = QLabel("👤")
        icon.setStyleSheet("font-size: 20px; border: none;")
        layout.addWidget(icon)
        
        info_layout = QVBoxLayout()
        
        name = QLabel(self.member_data["username"])
        name.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        name.setStyleSheet("color: #333; border: none;")
        info_layout.addWidget(name)
        
        email = QLabel(self.member_data["email"])
        email.setStyleSheet("color: #888; font-size: 11px; border: none;")
        info_layout.addWidget(email)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        if self.member_data.get("is_owner"):
            owner_badge = QLabel("👑")
            owner_badge.setStyleSheet("font-size: 20px; border: none;")
            layout.addWidget(owner_badge)
        elif self.can_remove:
            remove_btn = QPushButton("Кик")
            remove_btn.setObjectName("danger")
            remove_btn.setFixedWidth(100)
            remove_btn.clicked.connect(lambda: self.remove_requested.emit(self.member_data))
            layout.addWidget(remove_btn)
