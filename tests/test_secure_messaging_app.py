import unittest
from unittest.mock import patch, MagicMock
from src.secure_messaging_app import send_message, receive_message

class TestSecureMessagingAppFunctions(unittest.TestCase):

    @patch('src.secure_messaging_app.encrypt_data_hybrid')
    @patch('src.secure_messaging_app.decrypt_data_hybrid')
    @patch('src.secure_messaging_app.data_manager.store_encrypted_data')
    @patch('src.secure_messaging_app.data_manager.retrieve_encrypted_data')
    @patch('src.secure_messaging_app.get_user_by_username')
    def test_send_and_receive_message_flow(self, mock_get_user, mock_retrieve, mock_store, mock_decrypt, mock_encrypt):
        sender_id = "alice"
        recipient_id = "bob"
        message_content = "Hello, Bob! This is a secure message."

        # Configure mocks
        mock_store.return_value = "mock_data_id_123"
        mock_retrieve.return_value = {
            'encrypted_content': b'\x00'*12 + b'\x00'*16 + b'encrypted_message_bytes',
            'encryption_metadata': {'recipient_username': recipient_id}
        }
        mock_get_user.side_effect = lambda username: {'id': username} if username in [sender_id, recipient_id] else None
        mock_encrypt.return_value = (b'encrypted_message_bytes', b'\x00'*12, b'\x00'*16) # ciphertext, nonce, tag
        mock_decrypt.return_value = message_content.encode('utf-8')

        # Test send_message
        returned_data_id = send_message(sender_id, recipient_id, message_content)
        self.assertEqual(returned_data_id, "mock_data_id_123")
        mock_store.assert_called_once_with(
            user_id=sender_id,
            data_type="secure_message",
            encrypted_content=b'\x00'*12 + b'\x00'*16 + b'encrypted_message_bytes',
            encryption_metadata={
                "algorithm": "hybrid_qkd",
                "sender_username": sender_id,
                "recipient_username": recipient_id,
                "original_message_length": len(message_content)
            }
        )

        # Test receive_message
        # Redirect stdout to capture print statements
        import sys
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output

        receive_message(recipient_id, returned_data_id)

        sys.stdout = sys.__stdout__ # Reset redirect

        mock_retrieve.assert_called_once_with(returned_data_id)
        mock_decrypt.assert_called_once_with(b'encrypted_message_bytes', b'\x00'*12, b'\x00'*16, b'\x00'*32)
        self.assertIn(f"Decrypted message: {message_content}", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()