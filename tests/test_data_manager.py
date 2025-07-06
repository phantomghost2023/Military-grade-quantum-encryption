import unittest
import os
import sys
import psycopg2
import json
from unittest.mock import patch, MagicMock

# Add the project root to the sys.path to allow absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.data_manager import DataManager
from src.database import init_db, get_db_connection
from src.config import Config

# Use a test database URL to avoid interfering with development database
TEST_DATABASE_URL = os.environ.get('TEST_DATABASE_URL', 'postgresql://postgres:@localhost:5432/test_quantum_encryption')

class TestDataManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Temporarily override the DATABASE_URL for testing
        cls._original_db_url = Config.DATABASE_URL
        Config.DATABASE_URL = TEST_DATABASE_URL

        # Ensure the test database exists and is clean
        cls._create_test_database()
        init_db() # Initialize tables in the test database

    @classmethod
    def tearDownClass(cls):
        # Clean up the test database
        cls._drop_test_database()
        # Restore original DATABASE_URL
        Config.DATABASE_URL = cls._original_db_url

    @classmethod
    def _create_test_database(cls):
        # Connect to the default postgres database to create/drop the test database
        conn = None
        try:
            conn = psycopg2.connect(cls._original_db_url.rsplit('/', 1)[0] + '/postgres')
            conn.autocommit = True
            cur = conn.cursor()
            # Terminate all connections to the test database before dropping
            cur.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{TEST_DATABASE_URL.split('/')[-1]}';")
            cur.execute(f"DROP DATABASE IF EXISTS {TEST_DATABASE_URL.split('/')[-1]};")
            cur.execute(f"CREATE DATABASE {TEST_DATABASE_URL.split('/')[-1]};")
            cur.close()
        except psycopg2.Error as e:
            print(f"Error creating test database: {e}")
        finally:
            if conn: conn.close()

    @classmethod
    def _drop_test_database(cls):
        conn = None
        try:
            conn = psycopg2.connect(cls._original_db_url.rsplit('/', 1)[0] + '/postgres')
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{TEST_DATABASE_URL.split('/')[-1]}';")
            cur.execute(f"DROP DATABASE IF EXISTS {TEST_DATABASE_URL.split('/')[-1]};")
            cur.close()
        except psycopg2.Error as e:
            print(f"Error dropping test database: {e}")
        finally:
            if conn: conn.close()

    def setUp(self):
        self.data_manager = DataManager()
        # Clear tables before each test to ensure isolation
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM user_profiles;")
        cur.execute("DELETE FROM encrypted_data_store;")
        cur.execute("DELETE FROM users;")
        conn.commit()
        cur.close()
        conn.close()

    def _create_test_user(self, username="testuser", password="password", role="user"):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s) RETURNING id;",
                    (username, password, role))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return user_id

    # --- Test User Profile Management ---

    def test_create_and_get_user_profile(self):
        user_id = self._create_test_user()
        display_name = "Test User"
        profile_picture_url = "http://example.com/pic.jpg"
        preferences = {"theme": "dark", "notifications": True}

        created = self.data_manager.create_user_profile(user_id, display_name, profile_picture_url, preferences)
        self.assertTrue(created)

        profile = self.data_manager.get_user_profile(user_id)
        self.assertIsNotNone(profile)
        self.assertEqual(profile["user_id"], user_id)
        self.assertEqual(profile["display_name"], display_name)
        self.assertEqual(profile["profile_picture_url"], profile_picture_url)
        self.assertEqual(profile["preferences"], preferences)

    def test_update_user_profile(self):
        user_id = self._create_test_user()
        self.data_manager.create_user_profile(user_id, "Old Name")

        new_display_name = "New Name"
        updated = self.data_manager.update_user_profile(user_id, display_name=new_display_name)
        self.assertTrue(updated)

        profile = self.data_manager.get_user_profile(user_id)
        self.assertEqual(profile["display_name"], new_display_name)

        new_preferences = {"theme": "light"}
        updated = self.data_manager.update_user_profile(user_id, preferences=new_preferences)
        self.assertTrue(updated)
        profile = self.data_manager.get_user_profile(user_id)
        self.assertEqual(profile["preferences"], new_preferences)

    def test_delete_user_profile(self):
        user_id = self._create_test_user()
        self.data_manager.create_user_profile(user_id, "To Be Deleted")

        deleted = self.data_manager.delete_user_profile(user_id)
        self.assertTrue(deleted)

        profile = self.data_manager.get_user_profile(user_id)
        self.assertIsNone(profile)

    # --- Test Encrypted Data Store Management ---

    def test_store_and_retrieve_encrypted_data(self):
        user_id = self._create_test_user()
        data_type = "message"
        encrypted_content = b"\x01\x02\x03\x04\x05"
        encryption_metadata = {"alg": "AES256", "key_id": "abc"}

        data_id = self.data_manager.store_encrypted_data(user_id, data_type, encrypted_content, encryption_metadata)
        self.assertIsNotNone(data_id)

        retrieved_data = self.data_manager.retrieve_encrypted_data(data_id)
        self.assertIsNotNone(retrieved_data)
        self.assertEqual(retrieved_data["data_id"], data_id)
        self.assertEqual(retrieved_data["user_id"], user_id)
        self.assertEqual(retrieved_data["data_type"], data_type)
        self.assertEqual(retrieved_data["encrypted_content"], encrypted_content)
        self.assertEqual(retrieved_data["encryption_metadata"], encryption_metadata)

    def test_delete_encrypted_data(self):
        user_id = self._create_test_user()
        data_id = self.data_manager.store_encrypted_data(user_id, "file", b"content", {"alg": "X"})
        self.assertIsNotNone(data_id)

        deleted = self.data_manager.delete_encrypted_data(data_id)
        self.assertTrue(deleted)

        retrieved_data = self.data_manager.retrieve_encrypted_data(data_id)
        self.assertIsNone(retrieved_data)

    def test_list_encrypted_data_by_user(self):
        user_id1 = self._create_test_user(username="user1")
        user_id2 = self._create_test_user(username="user2")

        self.data_manager.store_encrypted_data(user_id1, "message", b"msg1", {"alg": "A"})
        self.data_manager.store_encrypted_data(user_id1, "document", b"doc1", {"alg": "B"})
        self.data_manager.store_encrypted_data(user_id2, "message", b"msg2", {"alg": "C"})

        user1_data = self.data_manager.list_encrypted_data_by_user(user_id1)
        self.assertEqual(len(user1_data), 2)
        self.assertEqual(user1_data[0]["data_type"], "message") # Order might vary, but content should be there
        self.assertEqual(user1_data[1]["data_type"], "document")

        user1_messages = self.data_manager.list_encrypted_data_by_user(user_id1, data_type="message")
        self.assertEqual(len(user1_messages), 1)
        self.assertEqual(user1_messages[0]["data_type"], "message")

        user2_data = self.data_manager.list_encrypted_data_by_user(user_id2)
        self.assertEqual(len(user2_data), 1)
        self.assertEqual(user2_data[0]["data_type"], "message")

if __name__ == '__main__':
    unittest.main()
