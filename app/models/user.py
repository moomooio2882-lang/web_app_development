from .database import get_db

class User:
    @staticmethod
    def create(username, email, password_hash, role='user'):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            '''INSERT INTO users (username, email, password_hash, role) 
               VALUES (?, ?, ?, ?)''',
            (username, email, password_hash, role)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()

    @staticmethod
    def get_by_email(email):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return cursor.fetchone()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        return cursor.fetchall()
        
    @staticmethod
    def update(user_id, username, email):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'UPDATE users SET username = ?, email = ? WHERE id = ?',
            (username, email, user_id)
        )
        db.commit()

    @staticmethod
    def delete(user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        db.commit()
