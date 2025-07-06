import re

def validate_string(input_string, min_length=1, max_length=255, pattern=None):
    """Validates a string based on length and an optional regex pattern."""
    if not isinstance(input_string, str):
        return False, "Input must be a string."
    if not (min_length <= len(input_string) <= max_length):
        return False, f"String length must be between {min_length} and {max_length} characters."
    if pattern and not re.match(pattern, input_string):
        return False, "String does not match the required pattern."
    return True, "Validation successful."

def sanitize_string(input_string):
    """Sanitizes a string by removing leading/trailing whitespace and common script tags."""
    if not isinstance(input_string, str):
        return ""
    sanitized = input_string.strip()
    # Remove common script tags and HTML entities that could lead to XSS
    sanitized = re.sub(r'<script.*?>.*?</script>', '', sanitized, flags=re.IGNORECASE)
    sanitized = sanitized.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return sanitized

def validate_email(email):
    """Validates an email address format."""
    # Basic regex for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format."
    return True, "Validation successful."

def validate_password(password, min_length=8, require_digit=True, require_upper=True, require_lower=True, require_special=True):
    """Validates a password based on complexity requirements."""
    if not isinstance(password, str):
        return False, "Password must be a string."
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters long."
    if require_digit and not re.search(r'\d', password):
        return False, "Password must contain at least one digit."
    if require_upper and not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if require_lower and not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if require_special and not re.search(r'[!@#$%^&*(),.?\"{}|<>]', password):
        return False, "Password must contain at least one special character."
    return True, "Validation successful."

def validate_integer(input_int, min_value=None, max_value=None):
    """Validates an integer within an optional range."""
    if not isinstance(input_int, int):
        return False, "Input must be an integer."
    if min_value is not None and input_int < min_value:
        return False, f"Integer must be at least {min_value}.";
    if max_value is not None and input_int > max_value:
        return False, f"Integer must be at most {max_value}.";
    return True, "Validation successful."

def validate_boolean(input_bool):
    """Validates if the input is a boolean."""
    if not isinstance(input_bool, bool):
        return False, "Input must be a boolean."
    return True, "Validation successful."