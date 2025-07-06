import unittest
from unittest.mock import patch, MagicMock
from src.kms_api import KMSClient

class TestKMSAPI(unittest.TestCase):
    @patch('src.kms_api.requests.post')
    def test_generate_key(self, mock_post):
        mock_post.return_value.json.return_value = {'key_id': 'test_key_123', 'key_material': 'abc'}
        mock_post.return_value.status_code = 200

        client = KMSClient('http://localhost:8080')
        key_id, key_material = client.generate_key('AES256')

        self.assertEqual(key_id, 'test_key_123')
        self.assertEqual(key_material, 'abc')
        mock_post.assert_called_once_with('http://localhost:8080/generate_key', json={'algorithm': 'AES256'})

    @patch('src.kms_api.requests.post')
    def test_encrypt_data(self, mock_post):
        mock_post.return_value.json.return_value = {'encrypted_data': 'xyz'}
        mock_post.return_value.status_code = 200

        client = KMSClient('http://localhost:8080')
        encrypted_data = client.encrypt_data('test_key_123', 'some_data')

        self.assertEqual(encrypted_data, 'xyz')
        mock_post.assert_called_once_with('http://localhost:8080/encrypt', json={'key_id': 'test_key_123', 'data': 'some_data'})

    # Add more tests for decrypt_data, rotate_key, etc.

if __name__ == '__main__';
    unittest.main()