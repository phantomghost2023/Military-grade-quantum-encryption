import unittest
from src.pqc import Kyber, Dilithium

class TestPQC(unittest.TestCase):
    def test_kyber_kem(self):
        kyber = Kyber()
        public_key, private_key = kyber.generate_keypair()
        self.assertIsNotNone(public_key)
        self.assertIsNotNone(private_key)

        original_message = b"This is a quantum-safe secret."
        ciphertext, shared_secret_sender = kyber.encapsulate(public_key)
        self.assertIsNotNone(ciphertext)
        self.assertIsNotNone(shared_secret_sender)

        shared_secret_receiver = kyber.decapsulate(private_key, ciphertext)
        self.assertEqual(shared_secret_sender, shared_secret_receiver)

    def test_dilithium_dss(self):
        dilithium = Dilithium()
        verification_key, signing_key = dilithium.generate_keypair()
        self.assertIsNotNone(verification_key)
        self.assertIsNotNone(signing_key)

        message = "This is a message to be signed."
        signature = dilithium.sign(signing_key, message)
        self.assertIsNotNone(signature)

        is_valid = dilithium.verify(verification_key, message, signature)
        self.assertTrue(is_valid)

        # Test with invalid signature
        invalid_signature = b'\x00' * len(signature)  # Create a dummy invalid signature
        is_valid_invalid = dilithium.verify(verification_key, message, invalid_signature)
        self.assertFalse(is_valid_invalid)

    # Add more tests for different PQC algorithms, edge cases, etc.

if __name__ == '__main__':
    unittest.main()