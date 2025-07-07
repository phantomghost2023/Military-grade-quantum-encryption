import unittest
import datetime
from unittest.mock import patch, MagicMock
import jwt

from src.auth import hash_password, check_password, create_user, get_user_by_username, authenticate_user, generate_token, decode_token, verify_token, create_default_admin
from src.config import Config
from src.database import get_db_connection, init_db

class TestAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Ensure Config.SECRET_KEY is set for token tests
        Config.SECRET_KEY = "test_secret_key"

    def setUp(self):
        # Clean up database before each test
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS users CASCADE;")
        cur.execute("DROP TABLE IF EXISTS user_profiles CASCADE;")
        conn.commit()
        cur.close()
        conn.close()
        init_db()

    def tearDown(self):
        # Clean up database after each test
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS users CASCADE;")
        cur.execute("DROP TABLE IF EXISTS user_profiles CASCADE;")
        conn.commit()
        cur.close()
        conn.close()

    def test_hash_and_check_password(self):
        password = "mysecretpassword"
        hashed = hash_password(password)
        self.assertIsNotNone(hashed)
        self.assertTrue(check_password(password, hashed))
        self.assertFalse(check_password("wrongpassword", hashed))

    def test_create_user(self):
        user_id = create_user("testuser", "password123")
        self.assertIsNotNone(user_id)
        user = get_user_by_username("testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "testuser")
        self.assertEqual(user['role'], 'user')

    def test_create_user_with_role(self):
        user_id = create_user("adminuser", "adminpass", role='admin')
        self.assertIsNotNone(user_id)
        user = get_user_by_username("adminuser")
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "adminuser")
        self.assertEqual(user['role'], 'admin')

    def test_create_user_duplicate(self):
        create_user("testuser", "password123")
        # Attempt to create user with same username, should return None
        user_id = create_user("testuser", "password456")
        self.assertIsNone(user_id)

    def test_get_user_by_username(self):
        create_user("testuser", "password123")
        user = get_user_by_username("testuser")
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "testuser")
        self.assertIn('password_hash', user)

        non_existent_user = get_user_by_username("nonexistent")
        self.assertIsNone(non_existent_user)

    def test_authenticate_user(self):
        create_user("testuser", "password123")
        user = authenticate_user("testuser", "password123")
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "testuser")

    def test_authenticate_user_invalid_password(self):
        create_user("testuser", "password123")
        user = authenticate_user("testuser", "wrongpassword")
        self.assertIsNone(user)

    def test_authenticate_user_non_existent(self):
        user = authenticate_user("nonexistent", "password123")
        self.assertIsNone(user)

    def test_generate_and_decode_token(self):
        user_id = create_user("tokenuser", "tokenpass")
        token = generate_token(user_id, "tokenuser", "user")
        self.assertIsNotNone(token)
        decoded_payload = decode_token(token)
        self.assertIsNotNone(decoded_payload)
        self.assertEqual(decoded_payload['user_id'], user_id)
        self.assertEqual(decoded_payload['username'], "tokenuser")
        self.assertEqual(decoded_payload['role'], "user")

    def test_decode_token_expired(self):
        user_id = create_user("expireduser", "expiredpass")
        # Manually create an expired token
        expired_payload = {
            'user_id': user_id,
            'username': "expireduser",
            'role': "user",
            'exp': datetime.datetime.utcnow() - datetime.timedelta(seconds=1)
        }
        expired_token = jwt.encode(expired_payload, Config.SECRET_KEY, algorithm='HS256')
        decoded_payload = decode_token(expired_token)
        self.assertIn('error', decoded_payload)
        self.assertEqual(decoded_payload['error'], 'Token has expired')

    def test_decode_token_invalid(self):
        invalid_token = "invalid.token.string"
        decoded_payload = decode_token(invalid_token)
        self.assertIn('error', decoded_payload)
        self.assertEqual(decoded_payload['error'], 'Invalid token')

    def test_verify_token_valid(self):
        user_id = create_user("verifyuser", "verifypass")
        token = generate_token(user_id, "verifyuser", "user")
        verified_payload = verify_token(token)
        self.assertIsNotNone(verified_payload)
        self.assertEqual(verified_payload['username'], "verifyuser")

    def test_verify_token_invalid(self):
        invalid_token = "invalid.token.string"
        verified_payload = verify_token(invalid_token)
        self.assertIsNone(verified_payload)

    def test_create_default_admin(self):
        # Ensure no admin exists initially
        self.assertIsNone(get_user_by_username("admin"))
        create_default_admin()
        admin_user = get_user_by_username("admin")
        self.assertIsNotNone(admin_user)
        self.assertEqual(admin_user['username'], "admin")
        self.assertEqual(admin_user['role'], 'admin')

        # Test calling it again, should not create a duplicate
        create_default_admin()
        admin_users = []
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username = %s;", ("admin",))
        for row in cur.fetchall():
            admin_users.append(row[0])
        cur.close()
        conn.close()
        self.assertEqual(len(admin_users), 1)

if __name__ == '__main__':
    unittest.main()