import sqlite3
import bcrypt
import json
from datetime import datetime
import os

class Database:
    def __init__(self, db_path="agent1.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Chat sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT DEFAULT 'New Chat',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                system_prompt TEXT,
                character_image TEXT DEFAULT 'default.png',
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_sessions (id)
            )
        ''')
        
        # User memory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def verify_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result and bcrypt.checkpw(password.encode('utf-8'), result[1]):
            return result[0]
        return None
    
    def create_chat_session(self, user_id, title="New Chat", system_prompt="", character_image="default.png"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO chat_sessions (user_id, title, system_prompt, character_image) VALUES (?, ?, ?, ?)",
            (user_id, title, system_prompt, character_image)
        )
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id
    
    def get_user_sessions(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, title, created_at, system_prompt, character_image FROM chat_sessions WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        sessions = cursor.fetchall()
        conn.close()
        return sessions
    
    def add_message(self, session_id, role, content):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content)
        )
        conn.commit()
        conn.close()
    
    def get_session_messages(self, session_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role, content, timestamp FROM messages WHERE session_id = ? ORDER BY timestamp ASC",
            (session_id,)
        )
        messages = cursor.fetchall()
        conn.close()
        return messages
    
    def update_session_character(self, session_id, character_image):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE chat_sessions SET character_image = ? WHERE id = ?",
            (character_image, session_id)
        )
        conn.commit()
        conn.close()
    
    def update_session_system_prompt(self, session_id, system_prompt):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE chat_sessions SET system_prompt = ? WHERE id = ?",
            (system_prompt, session_id)
        )
        conn.commit()
        conn.close()
    
    def set_user_memory(self, user_id, key, value):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT OR REPLACE INTO user_memory (user_id, key, value) VALUES (?, ?, ?)",
            (user_id, key, value)
        )
        conn.commit()
        conn.close()
    
    def get_user_memory(self, user_id, key):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT value FROM user_memory WHERE user_id = ? AND key = ?",
            (user_id, key)
        )
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

# Global database instance
db = Database()
