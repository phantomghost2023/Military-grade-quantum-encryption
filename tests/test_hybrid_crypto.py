import unittest
from src.hybrid_crypto import generate_hybrid_keys, encrypt_hybrid, decrypt_hybrid

class TestHybridCrypto(unittest.TestCase):
    def test_hybrid_encryption_decryption(self):
        # Generate hybrid keys
        public_key, private_key = generate_hybrid_keys()
        self.assertIsNotNone(public_key)
        self.assertIsNotNone(private_key)

        # Test encryption and decryption
        original_message = "This is a secret message."
        encrypted_message = encrypt_hybrid(original_message, public_key)
        self.assertIsNotNone(encrypted_message)
        self.assertNotEqual(original_message, encrypted_message) # Ensure it's actually encrypted

        decrypted_message = decrypt_hybrid(encrypted_message, private_key)
        self.assertEqual(original_message, decrypted_message)

    # Add more tests for edge cases, invalid keys, etc.

if __name__ == '__main__';
    unittest.main()