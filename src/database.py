
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from src.config import Config
import os

def get_db_connection():
    conn = psycopg2.connect(Config.DATABASE_URL)
    return conn

def init_db():
    db_url = Config.DATABASE_URL
    db_name = db_url.split('/')[-1]
    
    # Connect to the default 'postgres' database to create the new database
    conn_postgres = None
    try:
        # Create a database URL for the 'postgres' database
        postgres_db_url = os.path.dirname(db_url) + '/postgres'
        conn_postgres = psycopg2.connect(postgres_db_url)
        conn_postgres.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn_postgres.cursor()
        
        # Check if the database exists
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(f'CREATE DATABASE {db_name}')
            print(f"Database '{db_name}' created.")
        else:
            print(f"Database '{db_name}' already exists.")
            
        cur.close()
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        if conn_postgres:
            conn_postgres.close()

    # Now connect to the newly created database to create tables
    conn = None
    try:
        conn = get_db_connection() # This uses Config.DATABASE_URL to connect to 'quantum_encryption'
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
        print("Tables created successfully.")
        cur.close()
    except Exception as e:
        print(f"Error initializing database tables: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialization complete.")
