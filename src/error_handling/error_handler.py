"""This module defines custom exception classes and a centralized error handling mechanism."""
import datetime
import traceback
from src.automation.event_manager import EventManager
from src.error_handling.error_visualizer import ErrorVisualizer
from src.logging_tracing import CentralizedLogger, DistributedTracer
from src.error_handling.custom_exceptions import (
    BaseAppException,
    AuthenticationError,
    AuthorizationError,
    DatabaseError,
    ValidationError,
    ConfigurationError,
    NetworkError,
    QuantumError,
    KMSOperationError,
    AutomationError
)

# Initialize CentralizedLogger
logger = CentralizedLogger(name="ErrorHandlerLogger", level="ERROR")

# Initialize DistributedTracer (optional, for tracing error handling flow)
tracer = DistributedTracer()

_event_manager_instance = None
_error_visualizer_instance = None

def set_event_manager(manager: EventManager):
    global _event_manager_instance
    _event_manager_instance = manager

def set_error_visualizer(visualizer: ErrorVisualizer):
    global _error_visualizer_instance
    _error_visualizer_instance = visualizer




class ErrorHandler:
    """
    A class to provide a structured interface for handling errors.
    """
    @staticmethod
    def handle_error(
        e: Exception, 
        message: str = "An unexpected error occurred.", 
        level: str = "error",
        error_code: str = None,
        details: dict = None
    ):
        """
        Generic error handler that logs the error and raises a custom exception.
        Args:
            e (Exception): The original exception.
            message (str): A custom message to prepend to the error.
            level (str): The logging level ('debug', 'info', 'warning', 'error', 'critical').
        """
        full_message = f"{message} Original error: {e}"
        if error_code: full_message += f" (Code: {error_code})"
        if details: full_message += f" (Details: {details})"
        # Log the error using the CentralizedLogger, including stack trace
        log_method = getattr(logger, level, logger.error) # Get logging method based on level
        log_method(full_message, exc_info=True, stack_info=True, error_type=e.__class__.__name__, error_details=details, error_code=error_code)

        # Ensure level is valid for event emission
        if level not in ["debug", "info", "warning", "error", "critical"]:
            logger.error(
                "Invalid logging level specified: %s. Defaulting to error. %s",
                level, full_message
            )
            level = "error"

        # Determine error type for event payload
        error_type = e.__class__.__name__

        # Emit an event
        if _event_manager_instance:
            event_payload = {
                "error_type": error_type,
                "message": full_message,
                "level": level,
                "timestamp": datetime.datetime.now().isoformat(),
                "error_code": error_code,
                "details": details
            }
            if level == "critical":
                _event_manager_instance.emit_event("critical_error_alert", event_payload)
            else:
                _event_manager_instance.emit_event("error_detected", event_payload)
        else:
            logging.warning("EventManager not set in ErrorHandler. Cannot emit error event.")

        # Record error for visualization
        if _error_visualizer_instance:
            _error_visualizer_instance.add_error(error_type, datetime.datetime.now())

        # Re-raise a specific custom exception based on the original error or context
        if isinstance(e, AuthenticationError):
            raise AuthenticationError(message, details=details, error_code=error_code)
        elif isinstance(e, AuthorizationError):
            raise AuthorizationError(message, details=details, error_code=error_code)
        elif isinstance(e, DatabaseError):
            raise DatabaseError(message, details=details, error_code=error_code)
        elif isinstance(e, ValidationError):
            raise ValidationError(message, details=details, error_code=error_code)
        elif isinstance(e, ConfigurationError):
            raise ConfigurationError(message, details=details, error_code=error_code)
        elif isinstance(e, NetworkError):
            raise NetworkError(message, details=details, error_code=error_code)
        elif isinstance(e, QuantumError):
            raise QuantumError(message, details=details, error_code=error_code)
        elif isinstance(e, KMSOperationError):
            raise KMSOperationError(message, details=details, error_code=error_code)
        elif isinstance(e, AutomationError):
            raise AutomationError(message, details=details, error_code=error_code)
        elif isinstance(e, BaseAppException):
            # If the original exception is already a BaseAppException, re-raise it
            # but ensure its details are updated if new ones are provided.
            if details and not e.details:
                e.details = details
            if error_code and not e.error_code:
                e.error_code = error_code
            raise e
        else:
            # For any other unhandled exception, raise a generic BaseAppException
            raise BaseAppException(message, details=details, error_code=error_code)
