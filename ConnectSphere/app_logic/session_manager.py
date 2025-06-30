import hashlib
import os
SESSION_FILE = "session.txt"

def hash_password(password):
    """hashes password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def start_session(username, password):
    if os.path.exists(f"user_data/{username}.txt"):
        with open(f"user_data/{username}.txt", "r") as file:
            stored_password = file.readline().strip()
            if stored_password == password:
                with open(SESSION_FILE, "w") as session_file:
                    session_file.write(username)
                return True
    return False

def end_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        return True, "Logged out successfully!"
    return False, "Error logging out!"

def get_current_user():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as file:
            return file.readline().strip()
    return None
