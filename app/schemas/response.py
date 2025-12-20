from pydantic import BaseModel
from typing import Any, Optional

class BaseResponse(BaseModel):
    """基础响应模型，所有响应的统一结构"""
    code: int
    message: str
    request_id: str
    
    class Config:
        from_attributes = True

class SuccessResponse(BaseResponse):
    """成功响应模型"""
    data: Any = None
    
    class Config:
        arbitrary_types_allowed = True

class ErrorResponse(BaseResponse):
    """错误响应模型"""
    error_details: Optional[dict] = None
