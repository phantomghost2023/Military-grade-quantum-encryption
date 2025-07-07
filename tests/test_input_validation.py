import unittest
from src.input_validation import validate_email, validate_password, validate_string

class TestInputValidation(unittest.TestCase):
    def test_validate_email(self):
        self.assertTrue(validate_email('test@example.com'))
        self.assertFalse(validate_email('invalid-email')[0])

    def test_validate_password(self):
        self.assertTrue(validate_password('StrongP@ssw0rd'))
        self.assertFalse(validate_password('weak')[0])

if __name__ == '__main__':
    unittest.main()