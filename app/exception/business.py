from .base import BaseAppException

class BusinessException(BaseAppException):
    """业务逻辑异常"""
    def __init__(
        self,
        message: str = "业务逻辑错误",
        code: int = 400,
        error_details: dict = None,
        log_level: str = "warning"
    ):
        super().__init__(message, code, error_details, log_level)

class NotFoundException(BaseAppException):
    """资源不存在异常"""
    def __init__(
        self,
        message: str = "资源不存在",
        code: int = 404,
        error_details: dict = None,
        log_level: str = "info"
    ):
        super().__init__(message, code, error_details, log_level)
