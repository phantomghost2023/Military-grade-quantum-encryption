import unittest
from src.config import Config
from src.database import get_db_connection

class TestConfig(unittest.TestCase):
    def test_config_values(self):
        self.assertEqual(Config.DATABASE_URL, 'postgresql://postgres:@localhost:5432/quantum_encryption')
        self.assertEqual(Config.SECRET_KEY, 'super-secret-key')

    def test_config_type(self):
        self.assertIsInstance(Config.DATABASE_URL, str)
        self.assertIsInstance(Config.SECRET_KEY, str)

if __name__ == '__main__':
    unittest.main()