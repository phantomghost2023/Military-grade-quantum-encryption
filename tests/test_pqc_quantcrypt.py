"""
Unit tests for the Post-Quantum Cryptography (PQC) implementations in src/pqc.py.

This module tests the Kyber Key Encapsulation Mechanism (KEM) and Dilithium Digital Signature Scheme (DSS)
classes, ensuring their correct functionality across various security levels and handling of invalid inputs.
"""

import unittest
from src.pqc import Kyber, Dilithium

class TestKyberQuantCrypt(unittest.TestCase):
    def test_kyber_key_exchange(self):
        """Test the Kyber key encapsulation and decapsulation process."""
        for level in ["512", "768", "1024"]:
            with self.subTest(level=level):
                # Initialize Kyber with a specific security level
                kyber_instance = Kyber(security_level=level)
                
                # Generate key pair for Alice
                pk_alice, sk_alice = kyber_instance.generate_keypair()

                # Alice encapsulates a shared secret for Bob using Bob's public key
                ciphertext, shared_secret_alice = kyber_instance.encapsulate(pk_alice)

                # Bob decapsulates the shared secret using his private key
                shared_secret_bob = kyber_instance.decapsulate(sk_alice, ciphertext)

                # Assert that the shared secrets match and are valid
                self.assertEqual(shared_secret_alice, shared_secret_bob)
                self.assertIsInstance(shared_secret_alice, bytes)
                self.assertGreater(len(shared_secret_alice), 0)

    def test_kyber_invalid_security_level(self):
        """Test that Kyber raises ValueError for invalid security levels."""
        with self.assertRaises(ValueError):
            Kyber(security_level="invalid")

class TestDilithiumQuantCrypt(unittest.TestCase):
    def test_dilithium_signing_verification(self):
        """Test the Dilithium signing and verification process."""
        for level in ["44", "65", "87"]:
            with self.subTest(level=level):
                # Initialize Dilithium with a specific security level
                dilithium_instance = Dilithium(security_level=level)
                
                # Generate key pair
                vk, sk = dilithium_instance.generate_keypair()

                # Define a message and sign it
                message = "This is a test message for Dilithium signing.".encode('utf-8')
                signature = dilithium_instance.sign(sk, message)
                
                # Verify the valid signature
                is_valid = dilithium_instance.verify(vk, message, signature)

                # Assert properties of the generated signature
                self.assertIsInstance(signature, bytes)
                self.assertGreater(len(signature), 0)
                self.assertTrue(is_valid)

                # Test verification with a tampered message
                tampered_message = "This is a tampered message.".encode('utf-8')
                self.assertFalse(dilithium_instance.verify(vk, tampered_message, signature))

                # Test verification with a tampered signature
                tampered_signature = signature[:-1] + b'\x00'
                self.assertFalse(dilithium_instance.verify(vk, message, tampered_signature))

    def test_dilithium_invalid_security_level(self):
        """Test that Dilithium raises ValueError for invalid security levels."""
        with self.assertRaises(ValueError):
            Dilithium(security_level="invalid")

if __name__ == '__main__':
    unittest.main()