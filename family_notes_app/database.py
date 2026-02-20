
import sqlite3
import hashlib
import uuid
from datetime import datetime
from typing import Optional, List, Tuple
import os

class Database:
    def __init__(self, db_path: str = "family_notes.db"):
        self.db_path = db_path
        self.connection = None
        self.init_database()
    
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS spaces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                owner_id INTEGER NOT NULL,
                invite_code TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS space_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                space_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (space_id) REFERENCES spaces(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(space_id, user_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                space_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                author_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (space_id) REFERENCES spaces(id) ON DELETE CASCADE,
                FOREIGN KEY (author_id) REFERENCES users(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                note_id INTEGER,
                space_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE SET NULL,
                FOREIGN KEY (space_id) REFERENCES spaces(id) ON DELETE SET NULL
            )
        """)
        
        conn.commit()
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def generate_invite_code() -> str:
        return str(uuid.uuid4())[:8].upper()
    

    def register_user(self, username: str, password: str, email: str) -> Tuple[bool, str]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, password_hash, email)
            )
            conn.commit()
            return True, "Регистрация успешна!"
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                return False, "Пользователь с таким именем уже существует"
            elif "email" in str(e):
                return False, "Email уже используется"
            return False, "Ошибка регистрации"
    
    def login_user(self, username: str, password: str) -> Tuple[bool, Optional[dict]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT id, username, email FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        user = cursor.fetchone()
        
        if user:
            return True, {"id": user["id"], "username": user["username"], "email": user["email"]}
        return False, None
    
    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            return {"id": user["id"], "username": user["username"], "email": user["email"]}
        return None
    

    def create_space(self, name: str, description: str, owner_id: int) -> Tuple[bool, str, Optional[int]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        invite_code = self.generate_invite_code()
        
        try:
            cursor.execute(
                "INSERT INTO spaces (name, description, owner_id, invite_code) VALUES (?, ?, ?, ?)",
                (name, description, owner_id, invite_code)
            )
            space_id = cursor.lastrowid
            
            cursor.execute(
                "INSERT INTO space_members (space_id, user_id) VALUES (?, ?)",
                (space_id, owner_id)
            )
            
            conn.commit()
            
            self.log_action(owner_id, None, space_id, "CREATE_SPACE", f"Создано пространство: {name}")
            
            return True, invite_code, space_id
        except Exception as e:
            return False, str(e), None
    
    def get_user_spaces(self, user_id: int) -> List[dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.id, s.name, s.description, s.owner_id, s.invite_code, s.created_at,
                   u.username as owner_name
            FROM spaces s
            JOIN space_members sm ON s.id = sm.space_id
            JOIN users u ON s.owner_id = u.id
            WHERE sm.user_id = ?
            ORDER BY s.created_at DESC
        """, (user_id,))
        
        spaces = []
        for row in cursor.fetchall():
            spaces.append({
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "owner_id": row["owner_id"],
                "invite_code": row["invite_code"],
                "created_at": row["created_at"],
                "owner_name": row["owner_name"]
            })
        return spaces
    
    def get_space_by_invite_code(self, invite_code: str) -> Optional[dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM spaces WHERE invite_code = ?", (invite_code.upper(),))
        space = cursor.fetchone()
        
        if space:
            return dict(space)
        return None
    
    def join_space(self, user_id: int, invite_code: str) -> Tuple[bool, str]:
        space = self.get_space_by_invite_code(invite_code)
        
        if not space:
            return False, "Пространство не найдено"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO space_members (space_id, user_id) VALUES (?, ?)",
                (space["id"], user_id)
            )
            conn.commit()
            
            self.log_action(user_id, None, space["id"], "JOIN_SPACE", f"Присоединился к пространству")
            
            return True, f"Вы присоединились к пространству '{space['name']}'"
        except sqlite3.IntegrityError:
            return False, "Вы уже являетесь участником этого пространства"
    
    def get_space_members(self, space_id: int) -> List[dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.id, u.username, u.email, sm.joined_at, s.owner_id
            FROM users u
            JOIN space_members sm ON u.id = sm.user_id
            JOIN spaces s ON sm.space_id = s.id
            WHERE sm.space_id = ?
        """, (space_id,))
        
        members = []
        for row in cursor.fetchall():
            members.append({
                "id": row["id"],
                "username": row["username"],
                "email": row["email"],
                "joined_at": row["joined_at"],
                "is_owner": row["id"] == row["owner_id"]
            })
        return members
    
    def remove_member(self, space_id: int, user_id: int, remover_id: int) -> Tuple[bool, str]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT owner_id FROM spaces WHERE id = ?", (space_id,))
        space = cursor.fetchone()
        
        if not space:
            return False, "Пространство не найдено"
        
        if space["owner_id"] != remover_id:
            return False, "Только владелец может исключать участников"
        
        if user_id == remover_id:
            return False, "Вы не можете исключить себя"
        
        cursor.execute(
            "DELETE FROM space_members WHERE space_id = ? AND user_id = ?",
            (space_id, user_id)
        )
        conn.commit()
        
        self.log_action(remover_id, None, space_id, "REMOVE_MEMBER", f"Исключен пользователь ID: {user_id}")
        
        return True, "Участник исключён"
    
    def delete_space(self, space_id: int, user_id: int) -> Tuple[bool, str]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT owner_id FROM spaces WHERE id = ?", (space_id,))
        space = cursor.fetchone()
        
        if not space:
            return False, "Пространство не найдено"
        
        if space["owner_id"] != user_id:
            return False, "Только владелец может удалить пространство"
        
        cursor.execute("DELETE FROM spaces WHERE id = ?", (space_id,))
        conn.commit()
        
        return True, "Пространство удалено"
    

    def create_note(self, space_id: int, title: str, content: str, author_id: int) -> Tuple[bool, str]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO notes (space_id, title, content, author_id) VALUES (?, ?, ?, ?)",
                (space_id, title, content, author_id)
            )
            note_id = cursor.lastrowid
            conn.commit()
            
            self.log_action(author_id, note_id, space_id, "CREATE_NOTE", f"Создана заметка: {title}")
            
            return True, "Заметка создана"
        except Exception as e:
            return False, str(e)
    
    def get_space_notes(self, space_id: int) -> List[dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT n.*, u.username as author_name
            FROM notes n
            JOIN users u ON n.author_id = u.id
            WHERE n.space_id = ?
            ORDER BY n.updated_at DESC
        """, (space_id,))
        
        notes = []
        for row in cursor.fetchall():
            notes.append({
                "id": row["id"],
                "title": row["title"],
                "content": row["content"],
                "author_id": row["author_id"],
                "author_name": row["author_name"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            })
        return notes
    
    def update_note(self, note_id: int, title: str, content: str, user_id: int) -> Tuple[bool, str]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT space_id FROM notes WHERE id = ?", (note_id,))
        note = cursor.fetchone()
        
        if not note:
            return False, "Заметка не найдена"
        
        cursor.execute(
            "UPDATE notes SET title = ?, content = ?, updated_at = ? WHERE id = ?",
            (title, content, datetime.now(), note_id)
        )
        conn.commit()
        
        self.log_action(user_id, note_id, note["space_id"], "UPDATE_NOTE", f"Обновлена заметка: {title}")
        
        return True, "Заметка обновлена"
    
    def delete_note(self, note_id: int, user_id: int) -> Tuple[bool, str]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT space_id, title FROM notes WHERE id = ?", (note_id,))
        note = cursor.fetchone()
        
        if not note:
            return False, "Заметка не найдена"
        
        self.log_action(user_id, note_id, note["space_id"], "DELETE_NOTE", f"Удалена заметка: {note['title']}")
        
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        
        return True, "Заметка удалена"
    

    def log_action(self, user_id: int, note_id: Optional[int], space_id: Optional[int], 
                   action: str, details: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO activity_logs (user_id, note_id, space_id, action, details) VALUES (?, ?, ?, ?, ?)",
            (user_id, note_id, space_id, action, details)
        )
        conn.commit()
    
    def get_space_logs(self, space_id: int, limit: int = 50) -> List[dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT al.*, u.username
            FROM activity_logs al
            JOIN users u ON al.user_id = u.id
            WHERE al.space_id = ?
            ORDER BY al.timestamp DESC
            LIMIT ?
        """, (space_id, limit))
        
        logs = []
        for row in cursor.fetchall():
            logs.append({
                "id": row["id"],
                "username": row["username"],
                "action": row["action"],
                "details": row["details"],
                "timestamp": row["timestamp"]
            })
        return logs
    
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
