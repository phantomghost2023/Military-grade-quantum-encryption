import unittest
from src.kms_api import KMS
import os

class TestKMSAPI(unittest.TestCase):
    def test_generate_pqc_key_pair(self):
        kms = KMS()
        key_info = kms.generate_pqc_key_pair('test_kyber_key', algorithm='Kyber')
        self.assertIsNotNone(key_info)
        self.assertEqual(key_info['algorithm'], 'Kyber')
        self.assertIn('public_key', key_info)
        self.assertIn('private_key', key_info)

    def test_encrypt_decrypt_data_with_kms_key(self):
        kms = KMS()
        # Generate a symmetric key first
        sym_key_info = kms.generate_symmetric_key('test_sym_key')
        self.assertIsNotNone(sym_key_info)

        original_data = b"This is a secret message."
        ciphertext, nonce, tag = kms.encrypt_data_with_kms_key('test_sym_key', original_data)
        self.assertIsNotNone(ciphertext)
        self.assertIsNotNone(nonce)
        self.assertIsNotNone(tag)

        decrypted_data = kms.decrypt_data_with_kms_key('test_sym_key', ciphertext, nonce, tag)
        self.assertEqual(original_data, decrypted_data)



    # Add more tests for decrypt_data, rotate_key, etc.

if __name__ == '__main__':
    unittest.main()