import sqlite3
import hashlib

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def authenticate(username, password):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role FROM users
        WHERE username=? AND password=?
    """, (username, hash_password(password)))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None
