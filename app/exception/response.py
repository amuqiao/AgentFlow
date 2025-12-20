from typing import Any, Optional
from app.schemas.response import SuccessResponse, ErrorResponse

class ResponseBuilder:
    """响应构建器，基于统一响应模型"""
    
    @staticmethod
    def success(data: Any = None, message: str = "success", code: int = 200, request_id: str = None) -> dict:
        """构建成功响应"""
        return SuccessResponse(
            code=code,
            message=message,
            data=data,
            request_id=request_id
        ).dict()
    
    @staticmethod
    def error(message: str, code: int, error_details: Optional[dict] = None, request_id: str = None) -> dict:
        """构建错误响应"""
        return ErrorResponse(
            code=code,
            message=message,
            error_details=error_details,
            request_id=request_id
        ).dict()
