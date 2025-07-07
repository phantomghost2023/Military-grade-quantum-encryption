import unittest
import psycopg2
from src.database import get_db_connection, init_db

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the database once for all tests
        init_db()

    def setUp(self):
        # Establish a new connection for each test
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

        # Clean up tables before each test to ensure a clean state
        self.cursor.execute("DROP TABLE IF EXISTS users CASCADE;")
        self.cursor.execute("DROP TABLE IF EXISTS user_profiles CASCADE;")
        self.cursor.execute("DROP TABLE IF EXISTS encrypted_data_store CASCADE;")
        self.conn.commit()
        init_db() # Re-initialize tables

    def tearDown(self):
        # Close the connection after each test
        if self.conn:
            self.cursor.close()
            self.conn.close()

    def test_get_db_connection(self):
        # Test if connection is established
        self.assertIsNotNone(self.conn)
        self.assertFalse(self.conn.closed)

    def test_init_db_creates_tables(self):
        # Verify that tables are created after init_db
        self.cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        tables = [row[0] for row in self.cursor.fetchall()]
        self.assertIn('users', tables)
        self.assertIn('user_profiles', tables)
        self.assertIn('encrypted_data_store', tables)

    def test_user_insertion(self):
        # Test inserting a user
        self.cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                            ('testuser', 'hashed_password', 'user'))
        self.conn.commit()

        self.cursor.execute("SELECT * FROM users WHERE username = 'testuser'")
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[1], 'testuser')

    def test_duplicate_username_insertion(self):
        # Test inserting a duplicate username (should raise an error)
        self.cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                            ('duplicate_user', 'hashed_password', 'user'))
        self.conn.commit()

        with self.assertRaises(psycopg2.errors.UniqueViolation):
            self.cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                                ('duplicate_user', 'hashed_password', 'user'))
            self.conn.commit()

if __name__ == '__main__':
    unittest.main()
