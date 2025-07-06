import unittest
import os
from src.cli_app import encrypt_file, decrypt_file
from src.secure_messaging_app import send_message, receive_message
from src.auth import create_user
from src.database import init_db

class TestE2EEncryption(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        create_user("Alice", "password123")
        create_user("Bob", "password123")

    def setUp(self):
        self.test_file_content = (
            b"This is a test message for encryption and decryption."
        )
        self.input_filepath = "test_input.txt"
        self.encrypted_filepath = "test_encrypted.bin"
        self.decrypted_filepath = "test_decrypted.txt"
        self.message_sender = "Alice"
        self.message_recipient = "Bob"
        self.test_message = "Hello, Bob! This is a secure message from Alice."

        with open(self.input_filepath, "wb") as f:
            f.write(self.test_file_content)

    def tearDown(self):
        if os.path.exists(self.input_filepath):
            os.remove(self.input_filepath)
        if os.path.exists(self.encrypted_filepath):
            os.remove(self.encrypted_filepath)
        if os.path.exists(self.decrypted_filepath):
            os.remove(self.decrypted_filepath)

    def test_file_encryption_decryption(self):
        print("\n--- Testing File Encryption/Decryption ---")
        encrypt_file(self.input_filepath, self.encrypted_filepath)
        self.assertTrue(os.path.exists(self.encrypted_filepath))

        decrypt_file(self.encrypted_filepath, self.decrypted_filepath)
        self.assertTrue(os.path.exists(self.decrypted_filepath))

        with open(self.decrypted_filepath, "rb") as f:
            decrypted_content = f.read()
        self.assertEqual(self.test_file_content, decrypted_content)
        print("File encryption/decryption test passed.")

    def test_secure_messaging(self):
        print("\n--- Testing Secure Messaging ---")
        data_id = send_message(
            self.message_sender, self.message_recipient, self.test_message
        )
        self.assertIsNotNone(data_id)
        self.assertIsInstance(data_id, str)

        receive_message(self.message_recipient, data_id)
        print("Secure messaging test passed.")


if __name__ == "__main__":
    unittest.main()
