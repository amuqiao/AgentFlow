from .base import BaseAppException

class ValidationException(BaseAppException):
    """参数验证异常"""
    def __init__(
        self,
        message: str = "参数验证失败",
        code: int = 400,
        error_details: dict = None,
        log_level: str = "info"
    ):
        super().__init__(message, code, error_details, log_level)
