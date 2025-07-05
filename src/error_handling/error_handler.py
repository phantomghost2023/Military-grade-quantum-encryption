import logging

# Configure logging
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


class QuantumEncryptionError(Exception):
    """Base exception for quantum encryption related errors."""

    pass


class KeyManagementError(QuantumEncryptionError):
    """Exception for errors related to key management operations."""

    pass


class QKDError(QuantumEncryptionError):
    """Exception for errors related to QKD simulation."""

    pass


class HybridEncryptionError(QuantumEncryptionError):
    """Exception for errors related to hybrid encryption/decryption."""

    pass


class DataIntegrityError(QuantumEncryptionError):
    """Exception for errors related to data integrity checks."""

    pass


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
        logging.debug(full_message)
    elif level == "info":
        logging.info(full_message)
    elif level == "warning":
        logging.warning(full_message)
    elif level == "error":
        logging.error(full_message)
    elif level == "critical":
        logging.critical(full_message)
    else:
        logging.error(
            f"Invalid logging level specified: {level}. Defaulting to error. {full_message}"
        )

    # Re-raise a specific custom exception based on the original error or context
    if isinstance(e, KeyManagementError):
        raise KeyManagementError(full_message)
    elif isinstance(e, QKDError):
        raise QKDError(full_message)
    elif isinstance(e, HybridEncryptionError):
        raise HybridEncryptionError(full_message)
    elif isinstance(e, DataIntegrityError):
        raise DataIntegrityError(full_message)
    else:
        raise QuantumEncryptionError(full_message)
