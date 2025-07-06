import unittest
from src.input_validation import validate_email, validate_password, ValidationError

class TestInputValidation(unittest.TestCase):
    def test_validate_email(self):
        self.assertTrue(validate_email('test@example.com'))
        self.assertFalse(validate_email('invalid-email'))
        with self.assertRaises(ValidationError):
            validate_email('invalid-email', raise_exception=True)

    def test_validate_password(self):
        self.assertTrue(validate_password('StrongP@ssw0rd'))
        self.assertFalse(validate_password('weak'))
        with self.assertRaises(ValidationError):
            validate_password('weak', raise_exception=True)

if __name__ == '__main__';
    unittest.main()