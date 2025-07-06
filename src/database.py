
import psycopg2
from src.config import Config

def get_db_connection():
    conn = psycopg2.connect(Config.DATABASE_URL)
    return conn

def init_db():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL DEFAULT 'user'
            );

            -- Enable uuid-ossp for UUID generation
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                display_name VARCHAR(100) NOT NULL,
                profile_picture_url VARCHAR(255),
                preferences JSONB,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS encrypted_data_store (
                data_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                data_type VARCHAR(50) NOT NULL,
                encrypted_content BYTEA NOT NULL,
                encryption_metadata JSONB NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized (users table created if not exists).")
