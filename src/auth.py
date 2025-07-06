
import bcrypt
import jwt
import datetime
from src.config import Config
from src.database import get_db_connection

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(username, password, role='user'):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        hashed_password = hash_password(password)
        cur.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s) RETURNING id;",
            (username, hashed_password, role)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()

        # Create a default user profile for the new user
        default_display_name = username  # Use username as default display name
        profile_created = data_manager.create_user_profile(user_id, default_display_name)
        if not profile_created:
            print(f"Warning: Failed to create profile for user {username}")

        return user_id
    except Exception as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_user_by_username(username):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, password_hash, role FROM users WHERE username = %s;", (username,))
        user = cur.fetchone()
        cur.close()
        if user:
            return {'id': user[0], 'username': user[1], 'password_hash': user[2], 'role': user[3]}
        return None
    except Exception as e:
        print(f"Error getting user by username: {e}")
        return None
    finally:
        if conn:
            conn.close()

def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user and check_password(password, user['password_hash']):
        return user
    return None

def generate_token(user_id, username, role):
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expires in 24 hours
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}

def create_default_admin():
    admin_username = "admin"
    admin_password = "admin_password" # Consider making this configurable or prompting for it

    if not get_user_by_username(admin_username):
        user_id = create_user(admin_username, admin_password, role='admin')
        if user_id:
            print(f"Default admin user '{admin_username}' created.")
        else:
            print(f"Failed to create default admin user '{admin_username}'.")
    else:
        print(f"Default admin user '{admin_username}' already exists.")

