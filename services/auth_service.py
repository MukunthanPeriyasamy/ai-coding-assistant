from backend.database.db_config import get_db_connection
from backend.utils.auth_utils import get_password_hash, verify_password, create_access_token
from backend.models.user import UserCreate, UserLogin
import sqlite3

def register_user(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    hashed_password = get_password_hash(user.password)
    
    try:
        cursor.execute(
            "INSERT INTO users (email, hashed_password, full_name) VALUES (?, ?, ?)",
            (user.email, hashed_password, user.full_name)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {"id": user_id, "email": user.email, "full_name": user.full_name}
    except sqlite3.IntegrityError:
        conn.close()
        return None

def authenticate_user(user_login: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (user_login.email,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return None
        
    if not verify_password(user_login.password, user['hashed_password']):
        return None
        
    return {
        "id": user['id'],
        "email": user['email'],
        "full_name": user['full_name']
    }
