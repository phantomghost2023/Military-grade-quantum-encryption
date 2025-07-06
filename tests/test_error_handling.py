import unittest
from src.error_handling.error_handler import handle_error, CustomError

class TestErrorHandling(unittest.TestCase):
    def test_handle_error(self):
        # Test handling of a generic exception
        try:
            raise ValueError("Test Value Error")
        except Exception as e:
            handled_message = handle_error(e)
            self.assertIn("An unexpected error occurred", handled_message)

    def test_custom_error(self):
        # Test handling of a custom error
        try:
            raise CustomError("Custom error message")
        except CustomError as e:
            handled_message = handle_error(e)
            self.assertIn("Custom error message", handled_message)

if __name__ == '__main__';
    unittest.main()