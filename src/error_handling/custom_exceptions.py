"""
Custom exception classes for the Military-grade-quantum-encryption project.
These exceptions provide more specific error types for better error handling and debugging.
"""

class BaseAppException(Exception):
    """Base exception for all custom application-specific errors."""
    def __init__(self, message="An application error occurred", details=None, error_code=None):
        super().__init__(message)
        self.details = details
        self.error_code = error_code

class AuthenticationError(BaseAppException):
    """Exception raised for authentication failures."""
    def __init__(self, message="Authentication failed", details=None, error_code=None):
        super().__init__(message, details, error_code)

class AuthorizationError(BaseAppException):
    """Exception raised for authorization failures (permission denied)."""
    def __init__(self, message="Authorization failed", details=None, error_code=None):
        super().__init__(message, details, error_code)

class DatabaseError(BaseAppException):
    """Exception raised for database-related errors."""
    def __init__(self, message="Database operation failed", details=None, error_code=None):
        super().__init__(message, details, error_code)

class ValidationError(BaseAppException):
    """Exception raised for input validation failures."""
    def __init__(self, message="Input validation failed", details=None, error_code=None):
        super().__init__(message, details, error_code)

class ConfigurationError(BaseAppException):
    """Exception raised for configuration-related errors."""
    def __init__(self, message="Configuration error", details=None, error_code=None):
        super().__init__(message, details, error_code)

class NetworkError(BaseAppException):
    """Exception raised for network communication errors."""
    def __init__(self, message="Network communication failed", details=None, error_code=None):
        super().__init__(message, details, error_code)

class QuantumError(BaseAppException):
    """Exception raised for quantum-specific errors (e.g., QKD, PQC)."""
    def __init__(self, message="Quantum operation failed", details=None, error_code=None):
        super().__init__(message, details, error_code)

class KMSOperationError(BaseAppException):
    """Exception raised for Key Management System (KMS) operation failures."""
    def __init__(self, message="KMS operation failed", details=None, error_code=None):
        super().__init__(message, details, error_code)

class AutomationError(BaseAppException):
    """Exception raised for automation engine or workflow failures."""
    def __init__(self, message="Automation task failed", details=None, error_code=None):
        super().__init__(message, details, error_code)