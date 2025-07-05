import unittest
from src.pqc_primitives import Kyber, Dilithium


class TestKyber(unittest.TestCase):
    def test_kyber_init(self):
        # Test initialization for different security levels
        kyber512 = Kyber(security_level=1)
        self.assertEqual(kyber512.security_level, 1)
        self.assertIn("n", kyber512.params)

        kyber768 = Kyber(security_level=2)
        self.assertEqual(kyber768.security_level, 2)
        self.assertIn("n", kyber768.params)

        kyber1024 = Kyber(security_level=3)
        self.assertEqual(kyber1024.security_level, 3)
        self.assertIn("n", kyber1024.params)

        # Test default security level
        kyber_default = Kyber()
        self.assertEqual(kyber_default.security_level, 3)

    def test_kyber_keypair_generation(self):
        kyber = Kyber(security_level=1)
        with self.assertRaises(NotImplementedError):
            kyber.generate_keypair()

    def test_kyber_encapsulation_decapsulation(self):
        kyber = Kyber(security_level=1)
        # These methods are placeholders, so we just test they don't crash
        kyber.encapsulate(None)
        kyber.decapsulate(None, None)


class TestDilithium(unittest.TestCase):
    def test_dilithium_init(self):
        # Test initialization for different security levels
        dilithium2 = Dilithium(security_level=2)
        self.assertEqual(dilithium2.security_level, 2)
        self.assertIn("n", dilithium2.params)

        dilithium3 = Dilithium(security_level=3)
        self.assertEqual(dilithium3.security_level, 3)
        self.assertIn("n", dilithium3.params)

        dilithium5 = Dilithium(security_level=5)
        self.assertEqual(dilithium5.security_level, 5)
        self.assertIn("n", dilithium5.params)

        # Test default security level
        dilithium_default = Dilithium()
        self.assertEqual(dilithium_default.security_level, 3)

    def test_dilithium_keypair_generation(self):
        dilithium = Dilithium(security_level=2)
        # This method is a placeholder, so we just test it doesn't crash
        dilithium.generate_keypair()

    def test_dilithium_signing_verification(self):
        dilithium = Dilithium(security_level=2)
        message = b"This is a test message."

        # Test signing (placeholder)
        dilithium.sign(None, message)

        # Test verification (raises NotImplementedError)
        with self.assertRaises(NotImplementedError):
            dilithium.verify(None, message, None)


if __name__ == "__main__":
    unittest.main()
