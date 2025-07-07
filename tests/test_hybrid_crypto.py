import unittest
import os
from src.hybrid_crypto import HybridCrypto

class TestHybridCrypto(unittest.TestCase):
    def test_hybrid_encryption_decryption(self):
        # Generate hybrid keys
        hybrid_crypto = HybridCrypto()
        qkd_key, kyber_ct, kyber_ss, kyber_pk = hybrid_crypto.hybrid_key_exchange()
        # For testing purposes, we'll use a simplified session key derivation
        session_key = hybrid_crypto._derive_key(qkd_key + kyber_ss, os.urandom(16), b"test-info", 32)
        self.assertIsNotNone(qkd_key)
        self.assertIsNotNone(kyber_ct)
        self.assertIsNotNone(kyber_ss)
        self.assertIsNotNone(kyber_pk)

        # Test encryption and decryption
        original_message = "This is a secret message."
        encrypted_message, nonce, tag = hybrid_crypto.encrypt_data(original_message.encode('utf-8'), session_key)
        self.assertIsNotNone(encrypted_message)
        self.assertNotEqual(original_message.encode('utf-8'), encrypted_message) # Ensure it's actually encrypted

        decrypted_message = hybrid_crypto.decrypt_data(encrypted_message, nonce, tag, session_key).decode('utf-8')
        self.assertEqual(original_message, decrypted_message)

    # Add more tests for edge cases, invalid keys, etc.

if __name__ == '__main__':
    unittest.main()