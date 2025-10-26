"""
Custom exceptions for PyOmron FINS
"""

class FinsError(Exception):
    """Base exception for FINS protocol errors"""
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code

class ConnectionError(FinsError):
    """Exception raised when connection to PLC fails"""
    pass

class TimeoutError(FinsError):
    """Exception raised when operation times out"""
    pass

class ReadError(FinsError):
    """Exception raised when read operation fails"""
    pass

class WriteError(FinsError):
    """Exception raised when write operation fails"""
    pass

class InvalidAddressError(FinsError):
    """Exception raised when address format is invalid"""
    pass