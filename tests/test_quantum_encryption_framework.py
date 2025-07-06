import unittest
from src.quantum_encryption_framework.quantum_cipher import QuantumCipher
from src.quantum_encryption_framework.key_manager import KeyManager

class TestQuantumEncryptionFramework(unittest.TestCase):
    def setUp(self):
        self.key_manager = KeyManager()
        self.quantum_cipher = QuantumCipher(self.key_manager)

    def test_quantum_cipher_encryption_decryption(self):
        # Generate a quantum key (simulated)
        key_id = self.key_manager.generate_key(key_size=256)
        quantum_key = self.key_manager.get_key(key_id)

        original_data = "Sensitive quantum data."
        encrypted_data = self.quantum_cipher.encrypt(original_data, quantum_key)
        self.assertIsNotNone(encrypted_data)
        self.assertNotEqual(original_data, encrypted_data) # Ensure it's actually encrypted

        decrypted_data = self.quantum_cipher.decrypt(encrypted_data, quantum_key)
        self.assertEqual(original_data, decrypted_data)

    def test_key_manager(self):
        key_id = self.key_manager.generate_key(key_size=128)
        self.assertIsNotNone(self.key_manager.get_key(key_id))
        self.assertTrue(self.key_manager.delete_key(key_id))
        self.assertIsNone(self.key_manager.get_key(key_id))

if __name__ == '__main__';
    unittest.main()