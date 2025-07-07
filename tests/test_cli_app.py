import unittest
from unittest.mock import patch, mock_open
from src.cli_app import encrypt_file, decrypt_file, main
import os

class TestCLIApp(unittest.TestCase):
    def setUp(self):
        self.input_file = "test_input.txt"
        self.encrypted_file = "test_encrypted.bin"
        self.decrypted_file = "test_decrypted.txt"
        with open(self.input_file, "w") as f:
            f.write("This is a test string.")

    def tearDown(self):
        for f in [self.input_file, self.encrypted_file, self.decrypted_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_encrypt_file(self):
        encrypt_file(self.input_file, self.encrypted_file)
        self.assertTrue(os.path.exists(self.encrypted_file))
        with open(self.encrypted_file, "rb") as f:
            content = f.read()
            self.assertGreater(len(content), 0)

    def test_decrypt_file(self):
        # First encrypt a file
        encrypt_file(self.input_file, self.encrypted_file)
        self.assertTrue(os.path.exists(self.encrypted_file))

        # Then decrypt it
        decrypt_file(self.encrypted_file, self.decrypted_file)
        self.assertTrue(os.path.exists(self.decrypted_file))

        with open(self.decrypted_file, "r") as f:
            content = f.read()
            self.assertEqual(content, "This is a test string.")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.cli_app.encrypt_file')
    def test_main_encrypt(self, mock_encrypt_file, mock_parse_args):
        mock_parse_args.return_value.action = 'encrypt'
        mock_parse_args.return_value.input = self.input_file
        mock_parse_args.return_value.output = self.encrypted_file
        main()
        mock_encrypt_file.assert_called_once_with(self.input_file, self.encrypted_file)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.cli_app.decrypt_file')
    def test_main_decrypt(self, mock_decrypt_file, mock_parse_args):
        mock_parse_args.return_value.action = 'decrypt'
        mock_parse_args.return_value.input = self.encrypted_file
        mock_parse_args.return_value.output = self.decrypted_file
        main()
        mock_decrypt_file.assert_called_once_with(self.encrypted_file, self.decrypted_file)

if __name__ == '__main__':
    unittest.main()