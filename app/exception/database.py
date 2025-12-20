from .base import BaseAppException

class DatabaseException(BaseAppException):
    """数据库异常"""
    def __init__(
        self,
        message: str = "数据库操作失败",
        code: int = 500,
        error_details: dict = None,
        log_level: str = "error"
    ):
        super().__init__(message, code, error_details, log_level)
