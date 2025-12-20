class BaseAppException(Exception):
    """应用基础异常类"""
    def __init__(
        self,
        message: str = "服务器内部错误",
        code: int = 500,
        error_details: dict = None,
        log_level: str = "error"
    ):
        self.message = message
        self.code = code
        self.error_details = error_details or {}
        self.log_level = log_level
        super().__init__(self.message)
