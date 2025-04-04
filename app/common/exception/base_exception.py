class BaseException(Exception):
    """Base exception for our application"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
        
class BadRequestException(BaseException):
    """Raised when user is not authorized"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)

class UnauthorizedException(BaseException):
    """Raised when user is not authorized"""
    def __init__(self, message: str):
        super().__init__(message, status_code=401)

class ForbiddenException(BaseException):
    """Raised when user is not authorized"""
    def __init__(self, message: str):
        super().__init__(message, status_code=403)

class ResourceNotFoundException(BaseException):
    """Raised when a requested resource is not found"""
    def __init__(self, message: str):
        super().__init__(message, status_code=404)

class UnsupportedMediaTypeException(BaseException):
    """Raised when a requested media type is not supported"""
    def __init__(self, message: str):
        super().__init__(message, status_code=415)

class ValidationException(BaseException):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=422)

class InternalServerErrorException(BaseException):
    """Raised when an internal server error occurs"""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)