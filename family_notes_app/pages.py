
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QStackedWidget,
                             QScrollArea, QGridLayout, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QSizePolicy, QTabWidget)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from widgets import SpaceCard, NoteCard, MemberCard
from dialogs import (CreateSpaceDialog, JoinSpaceDialog, InviteCodeDialog, 
                     NoteDialog, ConfirmDialog)


class LoginPage(QWidget):
    login_success = pyqtSignal(dict)
    switch_to_register = pyqtSignal()
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        form_frame = QFrame()
        form_frame.setFixedSize(400, 350)
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(15)
        
        title = QLabel("🏠 Семейные заметки")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; border: none;")
        form_layout.addWidget(title)
        
        subtitle = QLabel("Вход в аккаунт")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666; border: none; margin-bottom: 10px;")
        form_layout.addWidget(subtitle)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("👤 Имя пользователя")
        self.username_input.setStyleSheet("border: 20px solid #ddd; border-radius: 80px; padding: 12px;")
        form_layout.addWidget(self.username_input)
        self.username_input.setMinimumHeight(40)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔒 Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("border: 20px solid #ddd; border-radius: 80px; padding: 12px;")
        form_layout.addWidget(self.password_input)
        
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: #dc3545; border: none;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()
        form_layout.addWidget(self.error_label)
        
        login_btn = QPushButton("Войти")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90d9;
                color: white;
                border: none;
                border-radius: 80px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        form_layout.addWidget(login_btn)
        
        register_layout = QHBoxLayout()
        register_label = QLabel("Нет аккаунта?")
        register_label.setStyleSheet("color: #666; border: none;")
        register_layout.addWidget(register_label)
        
        register_btn = QPushButton("Зарегистрироваться")
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #4a90d9;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #357abd;
            }
        """)
        register_btn.clicked.connect(self.switch_to_register.emit)
        register_layout.addWidget(register_btn)
        register_layout.addStretch()
        
        form_layout.addLayout(register_layout)
        
        layout.addWidget(form_frame)
        
        self.password_input.returnPressed.connect(self.handle_login)
        self.username_input.returnPressed.connect(self.password_input.setFocus)
    
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error("Заполните все поля")
            return
        
        success, user = self.db.login_user(username, password)
        
        if success:
            self.login_success.emit(user)
            self.clear_form()
        else:
            self.show_error("Неверное имя пользователя или пароль")
    
    def show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.show()
    
    def clear_form(self):
        self.username_input.clear()
        self.password_input.clear()
        self.error_label.hide()


class RegisterPage(QWidget):
    register_success = pyqtSignal()
    switch_to_login = pyqtSignal()
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        form_frame = QFrame()
        form_frame.setFixedSize(400, 450)
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 150px;
                border: 10px solid #e0e0e0;
            }
        """)
        
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(15)
        
        title = QLabel("📝 Регистрация")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; border: none;")
        form_layout.addWidget(title)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("👤 Имя пользователя")
        self.username_input.setStyleSheet("border: 20px solid #ddd; border-radius: 80px; padding: 12px;")
        form_layout.addWidget(self.username_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("📧 Email")
        self.email_input.setStyleSheet("border: 20px solid #ddd; border-radius: 80px; padding: 12px;")
        form_layout.addWidget(self.email_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔒 Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("border: 20px solid #ddd; border-radius: 80px; padding: 12px;")
        form_layout.addWidget(self.password_input)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("🔒 Подтвердите пароль")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setStyleSheet("border: 20px solid #ddd; border-radius: 80px; padding: 12px;")
        form_layout.addWidget(self.confirm_password_input)
        
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: #dc3545; border: none;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        form_layout.addWidget(self.error_label)
        
        register_btn = QPushButton("Зарегистрироваться")
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        register_btn.clicked.connect(self.handle_register)
        form_layout.addWidget(register_btn)
        
        login_layout = QHBoxLayout()
        login_label = QLabel("Уже есть аккаунт?")
        login_label.setStyleSheet("color: #666; border: none;")
        login_layout.addWidget(login_label)
        
        login_btn = QPushButton("Войти")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #4a90d9;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #357abd;
            }
        """)
        login_btn.clicked.connect(self.switch_to_login.emit)
        login_layout.addWidget(login_btn)
        login_layout.addStretch()
        
        form_layout.addLayout(login_layout)
        
        layout.addWidget(form_frame)
    
    def handle_register(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not username or not email or not password:
            self.show_error("Заполните все поля")
            return
        
        if len(username) < 3:
            self.show_error("Имя пользователя должно быть не менее 3 символов")
            return
        
        if "@" not in email or "." not in email:
            self.show_error("Введите корректный email")
            return
        
        if len(password) < 6:
            self.show_error("Пароль должен быть не менее 6 символов")
            return
        
        if password != confirm_password:
            self.show_error("Пароли не совпадают")
            return
        
        success, message = self.db.register_user(username, password, email)
        
        if success:
            QMessageBox.information(self, "Успех", "Регистрация успешна! Теперь войдите в систему.")
            self.register_success.emit()
            self.clear_form()
        else:
            self.show_error(message)
    
    def show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.show()
    
    def clear_form(self):
        self.username_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.error_label.hide()


class HomePage(QWidget):
    space_selected = pyqtSignal(dict)
    logout_requested = pyqtSignal()
    
    def __init__(self, db, user: dict):
        super().__init__()
        self.db = db
        self.user = user
        self.setup_ui()
        self.load_spaces()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        header_layout = QHBoxLayout()
        
        welcome_label = QLabel(f"👋 Привет, {self.user['username']}!")
        welcome_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header_layout.addWidget(welcome_label)
        
        header_layout.addStretch()
        
        logout_btn = QPushButton("🚪 Выйти")
        logout_btn.setObjectName("secondary")
        logout_btn.clicked.connect(self.logout_requested.emit)
        header_layout.addWidget(logout_btn)
        
        layout.addLayout(header_layout)
        
        action_layout = QHBoxLayout()
        
        create_btn = QPushButton("Создать пространство")
        create_btn.setObjectName("success")
        create_btn.clicked.connect(self.create_space)
        action_layout.addWidget(create_btn)
        
        join_btn = QPushButton("🔗 Присоединиться по коду")
        join_btn.clicked.connect(self.join_space)
        action_layout.addWidget(join_btn)
        
        action_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.setObjectName("secondary")
        refresh_btn.clicked.connect(self.load_spaces)
        action_layout.addWidget(refresh_btn)
        
        layout.addLayout(action_layout)
        
        spaces_title = QLabel("📁 Мои пространства")
        spaces_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(spaces_title)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.spaces_container = QWidget()
        self.spaces_layout = QVBoxLayout(self.spaces_container)
        self.spaces_layout.setSpacing(15)
        self.spaces_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll_area.setWidget(self.spaces_container)
        layout.addWidget(scroll_area)
    
    def load_spaces(self):
        while self.spaces_layout.count():
            item = self.spaces_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        spaces = self.db.get_user_spaces(self.user["id"])
        
        if not spaces:
            empty_label = QLabel("У вас пока нет пространств.\nСоздайте новое или присоединитесь по коду!")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("color: #888; font-size: 16px; padding: 10px;")
            self.spaces_layout.addWidget(empty_label)
        else:
            for space in spaces:
                is_owner = space["owner_id"] == self.user["id"]
                card = SpaceCard(space, is_owner)
                card.clicked.connect(self.space_selected.emit)
                self.spaces_layout.addWidget(card)
        
        self.spaces_layout.addStretch()
    
    def create_space(self):
        dialog = CreateSpaceDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if not data["name"]:
                QMessageBox.warning(self, "Ошибка", "Введите название пространства")
                return
            
            success, invite_code, space_id = self.db.create_space(
                data["name"], data["description"], self.user["id"]
            )
            
            if success:
                QMessageBox.information(
                    self, "Успех", 
                    f"Пространство создано!\nКод приглашения: {invite_code}"
                )
                self.load_spaces()
            else:
                QMessageBox.warning(self, "Ошибка", f"Не удалось создать пространство: {invite_code}")
    
    def join_space(self):
        dialog = JoinSpaceDialog(self)
        if dialog.exec():
            code = dialog.get_code()
            if not code:
                QMessageBox.warning(self, "Ошибка", "Введите код приглашения")
                return
            
            success, message = self.db.join_space(self.user["id"], code)
            
            if success:
                QMessageBox.information(self, "Успех", message)
                self.load_spaces()
            else:
                QMessageBox.warning(self, "Ошибка", message)
    
    def update_user(self, user: dict):
        self.user = user
        self.load_spaces()


class SpacePage(QWidget):
    back_requested = pyqtSignal()
    
    def __init__(self, db, user: dict, space: dict):
        super().__init__()
        self.db = db
        self.user = user
        self.space = space
        self.is_owner = space["owner_id"] == user["id"]
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Верхняя панель
        header_layout = QHBoxLayout()
        
        back_btn = QPushButton("← Назад")
        back_btn.setObjectName("secondary")
        back_btn.clicked.connect(self.back_requested.emit)
        header_layout.addWidget(back_btn)
        
        space_title = QLabel(f"📁 {self.space['name']}")
        space_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header_layout.addWidget(space_title)
        
        if self.is_owner:
            owner_badge = QLabel("👑 Владелец")
            owner_badge.setStyleSheet("""
                background-color: #ffd700;
                color: #333;
                padding: 5px 10px;
                border-radius: 12px;
                font-size: 12px;
            """)
            header_layout.addWidget(owner_badge)
        
        header_layout.addStretch()
        
        invite_btn = QPushButton("📤 Пригласить")
        invite_btn.clicked.connect(self.show_invite_code)
        header_layout.addWidget(invite_btn)
        
        if self.is_owner:
            delete_space_btn = QPushButton("🗑️ Удалить пространство")
            delete_space_btn.setObjectName("danger")
            delete_space_btn.clicked.connect(self.delete_space)
            header_layout.addWidget(delete_space_btn)
        
        layout.addLayout(header_layout)
        
        self.tabs = QTabWidget()
        
        self.notes_tab = QWidget()
        self.setup_notes_tab()
        self.tabs.addTab(self.notes_tab, "📝 Заметки")
        
        self.members_tab = QWidget()
        self.setup_members_tab()
        self.tabs.addTab(self.members_tab, "👥 Участники")
        
        self.logs_tab = QWidget()
        self.setup_logs_tab()
        self.tabs.addTab(self.logs_tab, "📋 История")
        
        layout.addWidget(self.tabs)
        
        self.tabs.currentChanged.connect(self.on_tab_changed)
    
    def setup_notes_tab(self):
        layout = QVBoxLayout(self.notes_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        action_layout = QHBoxLayout()
        
        add_note_btn = QPushButton("Новая заметка")
        add_note_btn.setObjectName("success")
        add_note_btn.clicked.connect(self.create_note)
        action_layout.addWidget(add_note_btn)
        
        action_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.setObjectName("secondary")
        refresh_btn.clicked.connect(self.load_notes)
        action_layout.addWidget(refresh_btn)
        
        layout.addLayout(action_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.notes_container = QWidget()
        self.notes_layout = QVBoxLayout(self.notes_container)
        self.notes_layout.setSpacing(10)
        self.notes_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll_area.setWidget(self.notes_container)
        layout.addWidget(scroll_area)
    
    def setup_members_tab(self):
        layout = QVBoxLayout(self.members_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        info_label = QLabel(f"Код приглашения: {self.space['invite_code']}")
        info_label.setStyleSheet("color: #4a90d9; font-size: 14px; padding: 10px;")
        layout.addWidget(info_label)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.members_container = QWidget()
        self.members_layout = QVBoxLayout(self.members_container)
        self.members_layout.setSpacing(10)
        self.members_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        scroll_area.setWidget(self.members_container)
        layout.addWidget(scroll_area)
    
    def setup_logs_tab(self):
        layout = QVBoxLayout(self.logs_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.logs_table = QTableWidget()
        self.logs_table.setColumnCount(4)
        self.logs_table.setHorizontalHeaderLabels(["Время", "Пользователь", "Действие", "Детали"])
        self.logs_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.logs_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.logs_table.setAlternatingRowColors(True)

        layout.addWidget(self.logs_table)
    
    def load_data(self):
        self.load_notes()
        self.load_members()
        self.load_logs()
    
    def load_notes(self):
        while self.notes_layout.count():
            item = self.notes_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        notes = self.db.get_space_notes(self.space["id"])
        
        if not notes:
            empty_label = QLabel("Пока нет заметок. Создайте первую!")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("color: #888; font-size: 14px; padding: 30px;")
            self.notes_layout.addWidget(empty_label)
        else:
            for note in notes:
                card = NoteCard(note)
                card.edit_requested.connect(self.edit_note)
                card.delete_requested.connect(self.delete_note)
                self.notes_layout.addWidget(card)
        
        self.notes_layout.addStretch()
    
    def load_members(self):
        while self.members_layout.count():
            item = self.members_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        members = self.db.get_space_members(self.space["id"])
        
        for member in members:
            can_remove = self.is_owner and member["id"] != self.user["id"]
            card = MemberCard(member, can_remove)
            card.remove_requested.connect(self.remove_member)
            self.members_layout.addWidget(card)
        
        self.members_layout.addStretch()
    
    def load_logs(self):
        logs = self.db.get_space_logs(self.space["id"])
        
        self.logs_table.setRowCount(len(logs))
        
        action_names = {
            "CREATE_SPACE": "Создание пространства",
            "JOIN_SPACE": "Присоединение",
            "REMOVE_MEMBER": "Исключение участника",
            "CREATE_NOTE": "Создание заметки",
            "UPDATE_NOTE": "Редактирование заметки",
            "DELETE_NOTE": "Удаление заметки"
        }
        
        for i, log in enumerate(logs):
            self.logs_table.setItem(i, 0, QTableWidgetItem(log["timestamp"][:19]))
            self.logs_table.setItem(i, 1, QTableWidgetItem(log["username"]))
            self.logs_table.setItem(i, 2, QTableWidgetItem(action_names.get(log["action"], log["action"])))
            self.logs_table.setItem(i, 3, QTableWidgetItem(log["details"]))
    
    def on_tab_changed(self, index):
        if index == 0:
            self.load_notes()
        elif index == 1:
            self.load_members()
        elif index == 2:
            self.load_logs()
    
    def create_note(self):
        dialog = NoteDialog(parent=self)
        if dialog.exec():
            data = dialog.get_data()
            if not data["title"]:
                QMessageBox.warning(self, "Ошибка", "Введите заголовок заметки")
                return
            
            success, message = self.db.create_note(
                self.space["id"], data["title"], data["content"], self.user["id"]
            )
            
            if success:
                self.load_notes()
            else:
                QMessageBox.warning(self, "Ошибка", message)
    
    def edit_note(self, note: dict):
        dialog = NoteDialog(note, parent=self)
        if dialog.exec():
            data = dialog.get_data()
            if not data["title"]:
                QMessageBox.warning(self, "Ошибка", "Введите заголовок заметки")
                return
            
            success, message = self.db.update_note(
                note["id"], data["title"], data["content"], self.user["id"]
            )
            
            if success:
                self.load_notes()
            else:
                QMessageBox.warning(self, "Ошибка", message)
    
    def delete_note(self, note: dict):
        dialog = ConfirmDialog(
            "Удаление заметки",
            f"Вы уверены, что хотите удалить заметку «{note['title']}»?",
            self
        )
        if dialog.exec():
            success, message = self.db.delete_note(note["id"], self.user["id"])
            
            if success:
                self.load_notes()
            else:
                QMessageBox.warning(self, "Ошибка", message)
    
    def remove_member(self, member: dict):
        dialog = ConfirmDialog(
            "Исключение участника",
            f"Вы уверены, что хотите исключить {member['username']}?",
            self
        )
        if dialog.exec():
            success, message = self.db.remove_member(
                self.space["id"], member["id"], self.user["id"]
            )
            
            if success:
                self.load_members()
                QMessageBox.information(self, "Успех", "Участник исключён")
            else:
                QMessageBox.warning(self, "Ошибка", message)
    
    def show_invite_code(self):
        dialog = InviteCodeDialog(self.space["name"], self.space["invite_code"], self)
        dialog.exec()
    
    def delete_space(self):
        dialog = ConfirmDialog(
            "Удаление пространства",
            f"Вы уверены, что хотите удалить пространство «{self.space['name']}»?\n\nВсе заметки будут удалены!",
            self
        )
        if dialog.exec():
            success, message = self.db.delete_space(self.space["id"], self.user["id"])
            
            if success:
                QMessageBox.information(self, "Успех", "Пространство удалено")
                self.back_requested.emit()
            else:
                QMessageBox.warning(self, "Ошибка", message)
