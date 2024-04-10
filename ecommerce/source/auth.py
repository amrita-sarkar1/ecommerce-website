import sqlite3
import bcrypt
from source.utils import generate_otp, send_otp  # (Optional for email OTP)
from source.database import Database

class Auth:

    def __init__(self):
        self.db = Database()

    def register(self, username, email, password):
        password_hash = bcrypt.hash(password)
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                           (username, email, password_hash))
            self.db.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username or email already exists

    def login(self, username_or_email, password):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ? OR email = ?",
                       (username_or_email, username_or_email))
        user = cursor.fetchone()
        if user and bcrypt.verify(password, user[1]):
            return user[0]  # User ID
        else:
            return None

    def verify_otp(self, email, otp):  # (Optional for email OTP)
        # Implement logic to check received OTP against generated OTP for email
        pass

    def generate_reset_password_token(self, email):  # (Optional)
        # Generate a token and store it in the database, send it to email
        pass

    def reset_password(self, token, new_password):  # (Optional)
        # Validate token, update password hash in database
        pass
