import unittest
from src.pqc import Kyber, Dilithium

class TestKyberQuantCrypt(unittest.TestCase):
    def test_kyber_key_exchange(self):
        for level in ["512", "768", "1024"]:
            with self.subTest(level=level):
                kyber_instance = Kyber(security_level=level)
                pk_alice, sk_alice = kyber_instance.generate_keypair()

                # Alice encapsulates a shared secret for Bob
                ciphertext, shared_secret_alice = kyber_instance.encapsulate(pk_alice)

                # Bob decapsulates the shared secret
                shared_secret_bob = kyber_instance.decapsulate(sk_alice, ciphertext)

                self.assertEqual(shared_secret_alice, shared_secret_bob)
                self.assertIsInstance(shared_secret_alice, bytes)
                self.assertGreater(len(shared_secret_alice), 0)

    def test_kyber_invalid_security_level(self):
        with self.assertRaises(ValueError):
            Kyber(security_level="invalid")

class TestDilithiumQuantCrypt(unittest.TestCase):
    def test_dilithium_signing_verification(self):
        for level in ["44", "65", "87"]:
            with self.subTest(level=level):
                dilithium_instance = Dilithium(security_level=level)
                vk, sk = dilithium_instance.generate_keypair()

                message = "This is a test message for Dilithium signing.".encode('utf-8')
                signature = dilithium_instance.sign(sk, message)
                is_valid = dilithium_instance.verify(vk, message, signature)

                self.assertIsInstance(signature, bytes)
                self.assertGreater(len(signature), 0)
                # Verify valid signature
                self.assertTrue(is_valid)

                # Test with tampered message
                tampered_message = "This is a tampered message.".encode('utf-8')
                self.assertFalse(dilithium_instance.verify(vk, tampered_message, signature))

                # Test with tampered signature
                tampered_signature = signature[:-1] + b'\x00'
                self.assertFalse(dilithium_instance.verify(vk, message, tampered_signature))

    def test_dilithium_invalid_security_level(self):
        with self.assertRaises(ValueError):
            Dilithium(security_level="invalid")

if __name__ == '__main__':
    unittest.main()