"""This module defines custom exception classes and a centralized error handling mechanism."""
import logging
import time
from src.automation.event_manager import EventManager
from src.error_handling.error_visualizer import ErrorVisualizer
import datetime

# Configure logging
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)

_event_manager_instance = None
_error_visualizer_instance = None

def set_event_manager(manager: EventManager):
    global _event_manager_instance
    _event_manager_instance = manager

def set_error_visualizer(visualizer: ErrorVisualizer):
    global _error_visualizer_instance
    _error_visualizer_instance = visualizer


class QuantumEncryptionError(Exception):
    """Base exception for quantum encryption related errors."""




class KeyManagementError(QuantumEncryptionError):
    """Exception for errors related to key management operations."""




class QKDError(QuantumEncryptionError):
    """Exception for errors related to QKD simulation."""


class HybridEncryptionError(QuantumEncryptionError):
    """Exception for errors related to hybrid encryption/decryption."""


class DataIntegrityError(QuantumEncryptionError):
    """Exception for errors related to data integrity checks."""


class ErrorHandler:
    """
    A class to provide a structured interface for handling errors.
    """
    @staticmethod
    def handle_error(
        e: Exception, message: str = "An unexpected error occurred.", level: str = "error"
    ):
        """
        Generic error handler that logs the error and raises a custom exception.
        Args:
            e (Exception): The original exception.
            message (str): A custom message to prepend to the error.
            level (str): The logging level ('debug', 'info', 'warning', 'error', 'critical').
        """
        full_message = f"{message} Original error: {e}"
        if level == "debug":
            logging.debug("%s", full_message)
        elif level == "info":
            logging.info("%s", full_message)
        elif level == "warning":
            logging.warning("%s", full_message)
        elif level == "error":
            logging.error("%s", full_message)
        elif level == "critical":
            logging.critical("%s", full_message)
        else:
            logging.error(
                "Invalid logging level specified: %s. Defaulting to error. %s",
                level, full_message
            )
            level = "error" # Ensure level is valid for event emission

        # Determine error type for event payload
        error_type = e.__class__.__name__

        # Emit an event
        if _event_manager_instance:
            event_payload = {
                "error_type": error_type,
                "message": full_message,
                "level": level,
                "timestamp": datetime.datetime.now().isoformat()
            }
            if level == "critical":
                _event_manager_instance.emit_event("critical_error", event_payload)
            else:
                _event_manager_instance.emit_event("error_detected", event_payload)
        else:
            logging.warning("EventManager not set in ErrorHandler. Cannot emit error event.")

        # Record error for visualization
        if _error_visualizer_instance:
            _error_visualizer_instance.add_error(error_type, datetime.datetime.now())

        # Re-raise a specific custom exception based on the original error or context
        if isinstance(e, KeyManagementError):
            raise KeyManagementError(full_message)
        if isinstance(e, QKDError):
            raise QKDError(full_message)
        if isinstance(e, HybridEncryptionError):
            raise HybridEncryptionError(full_message)
        if isinstance(e, DataIntegrityError):
            raise DataIntegrityError(full_message)
        raise QuantumEncryptionError(full_message)
