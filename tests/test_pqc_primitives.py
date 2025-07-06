import unittest
from src.pqc import Kyber, Dilithium

class TestKyber(unittest.TestCase):
    def test_kyber_init(self):
        kyber512 = Kyber(security_level="512")
        self.assertIsInstance(kyber512, Kyber)
        self.assertEqual(kyber512.security_level, "512")

        with self.assertRaises(ValueError):
            Kyber(security_level="invalid")

    def test_kyber_keypair_generation(self):
        kyber = Kyber()
        pk, sk = kyber.generate_keypair()
        self.assertIsInstance(pk, bytes)
        self.assertIsInstance(sk, bytes)
        self.assertGreater(len(pk), 0)
        self.assertGreater(len(sk), 0)

    def test_kyber_encapsulation_decapsulation(self):
        kyber = Kyber()
        pk, sk = kyber.generate_keypair()
        ciphertext, shared_secret_sender = kyber.encapsulate(pk)
        shared_secret_receiver = kyber.decapsulate(sk, ciphertext)
        self.assertEqual(shared_secret_sender, shared_secret_receiver)
        self.assertIsInstance(shared_secret_sender, bytes)

class TestDilithium(unittest.TestCase):
    def test_dilithium_init(self):
        dilithium = Dilithium()
        self.assertIsInstance(dilithium, Dilithium)

    def test_dilithium_keypair_generation(self):
        dilithium = Dilithium()
        vk, sk = dilithium.generate_keypair()
        self.assertIsInstance(vk, bytes)
        self.assertIsInstance(sk, bytes)
        self.assertGreater(len(vk), 0)
        self.assertGreater(len(sk), 0)

    def test_dilithium_signing_verification(self):
        dilithium = Dilithium()
        vk, sk = dilithium.generate_keypair()
        message = b"test message"
        signature = dilithium.sign(sk, message)
        self.assertTrue(dilithium.verify(vk, message, signature))

        # Test with wrong message
        self.assertFalse(dilithium.verify(vk, b"wrong message", signature))

        # Test with wrong key
        vk_new, _ = dilithium.generate_keypair()
        self.assertFalse(dilithium.verify(vk_new, message, signature))


if __name__ == "__main__":
    unittest.main()
