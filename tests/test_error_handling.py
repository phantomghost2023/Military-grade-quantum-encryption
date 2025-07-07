import unittest
from unittest.mock import MagicMock, patch
from src.error_handling.error_handler import ErrorHandler, set_event_manager, set_error_visualizer
from src.error_handling.custom_exceptions import (
    BaseAppException,
    AuthenticationError,
    DatabaseError,
    ValidationError,
    NetworkError,
    QuantumError
)
from src.automation.event_manager import EventManager
from src.error_handling.error_visualizer import ErrorVisualizer

class TestErrorHandling(unittest.TestCase):

    def setUp(self):
        self.mock_event_manager = MagicMock(spec=EventManager)
        self.mock_error_visualizer = MagicMock(spec=ErrorVisualizer)
        set_event_manager(self.mock_event_manager)
        set_error_visualizer(self.mock_error_visualizer)

    def tearDown(self):
        set_event_manager(None)
        set_error_visualizer(None)

    @patch('src.error_handling.error_handler.logger')
    def test_generic_exception_handling(self, mock_logger):
        with self.assertRaises(BaseAppException) as cm:
            ErrorHandler.handle_error(ValueError("Something went wrong"), message="Generic test error")
        self.assertIn("Generic test error", str(cm.exception))
        mock_logger.error.assert_called_once()
        self.mock_event_manager.emit_event.assert_called_once_with(
            "error_detected",
            self.mock_event_manager.emit_event.call_args[0][1]
        )
        self.assertIsInstance(self.mock_event_manager.emit_event.call_args[0][1], dict)
        self.mock_error_visualizer.add_error.assert_called_once()

    @patch('src.error_handling.error_handler.logger')
    def test_authentication_error_re_raise(self, mock_logger):
        with self.assertRaises(AuthenticationError) as cm:
            ErrorHandler.handle_error(AuthenticationError("Invalid credentials"), message="Auth failed", error_code="AUTH_001")
        self.assertIn("Auth failed", str(cm.exception))
        self.assertEqual(cm.exception.error_code, "AUTH_001")
        mock_logger.error.assert_called_once()
        self.mock_event_manager.emit_event.assert_called_once()

    @patch('src.error_handling.error_handler.logger')
    def test_database_error_re_raise(self, mock_logger):
        with self.assertRaises(DatabaseError) as cm:
            ErrorHandler.handle_error(DatabaseError("DB connection failed"), message="DB error", details={"db_name": "test_db"})
        self.assertIn("DB error", str(cm.exception))
        self.assertEqual(cm.exception.details["db_name"], "test_db")
        mock_logger.error.assert_called_once()
        self.mock_event_manager.emit_event.assert_called_once()

    @patch('src.error_handling.error_handler.logger')
    def test_critical_error_event_emission(self, mock_logger):
        with self.assertRaises(BaseAppException):
            ErrorHandler.handle_error(Exception("Critical system failure"), level="critical", message="System down")
        self.mock_event_manager.emit_event.assert_called_once_with(
            "critical_error_alert",
            self.mock_event_manager.emit_event.call_args[0][1]
        )
        self.assertIsInstance(self.mock_event_manager.emit_event.call_args[0][1], dict)
        mock_logger.critical.assert_called_once()

    @patch('src.error_handling.error_handler.logger')
    def test_validation_error_re_raise(self, mock_logger):
        with self.assertRaises(ValidationError) as cm:
            ErrorHandler.handle_error(ValidationError("Invalid input"), message="Input validation failed", error_code="VAL_001")
        self.assertIn("Input validation failed", str(cm.exception))
        self.assertEqual(cm.exception.error_code, "VAL_001")
        mock_logger.error.assert_called_once()
        self.mock_event_manager.emit_event.assert_called_once()

    @patch('src.error_handling.error_handler.logger')
    def test_network_error_re_raise(self, mock_logger):
        with self.assertRaises(NetworkError) as cm:
            ErrorHandler.handle_error(NetworkError("Connection timed out"), message="Network issue", details={"host": "example.com"})
        self.assertIn("Network issue", str(cm.exception))
        self.assertEqual(cm.exception.details["host"], "example.com")
        mock_logger.error.assert_called_once()
        self.mock_event_manager.emit_event.assert_called_once()

    @patch('src.error_handling.error_handler.logger')
    def test_quantum_error_re_raise(self, mock_logger):
        with self.assertRaises(QuantumError) as cm:
            ErrorHandler.handle_error(QuantumError("Qubit decoherence"), message="Quantum computation error", error_code="QNT_001")
        self.assertIn("Quantum computation error", str(cm.exception))
        self.assertEqual(cm.exception.error_code, "QNT_001")
        mock_logger.error.assert_called_once()
        self.mock_event_manager.emit_event.assert_called_once()

if __name__ == '__main__':
    unittest.main()