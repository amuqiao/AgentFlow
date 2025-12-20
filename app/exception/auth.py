from .base import BaseAppException

class AuthException(BaseAppException):
    """认证异常"""
    def __init__(
        self,
        message: str = "认证失败",
        code: int = 401,
        error_details: dict = None,
        log_level: str = "warning"
    ):
        super().__init__(message, code, error_details, log_level)

class ForbiddenException(BaseAppException):
    """权限不足异常"""
    def __init__(
        self,
        message: str = "权限不足",
        code: int = 403,
        error_details: dict = None,
        log_level: str = "warning"
    ):
        super().__init__(message, code, error_details, log_level)
