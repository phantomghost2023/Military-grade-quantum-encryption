"""This module defines custom exception classes and a centralized error handling mechanism."""
import logging

# Configure logging
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


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

            logging.error(
                "Invalid logging level specified: %s. Defaulting to error. %s",
                level, full_message
            )

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
