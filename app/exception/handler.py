from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.exception.base import BaseAppException
from app.schemas.response import ErrorResponse
from app.config.logger import logger
from app.utils.request import get_request_id

async def custom_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    request_id = get_request_id(request)
    
    # 1. 处理自定义异常
    if isinstance(exc, BaseAppException):
        error_response = ErrorResponse(
            code=exc.code,
            message=exc.message,
            error_details=exc.error_details,
            request_id=request_id
        )
        log_level = exc.log_level
    
    # 2. 处理FastAPI参数验证异常
    elif isinstance(exc, RequestValidationError):
        error_details = {
            "errors": exc.errors(),
            "body": exc.body
        }
        error_response = ErrorResponse(
            code=status.HTTP_400_BAD_REQUEST,
            message="请求参数验证失败",
            error_details=error_details,
            request_id=request_id
        )
        log_level = "info"
    
    # 3. 处理Starlette HTTP异常
    elif isinstance(exc, StarletteHTTPException):
        error_response = ErrorResponse(
            code=exc.status_code,
            message=exc.detail,
            request_id=request_id
        )
        log_level = "warning" if exc.status_code < 500 else "error"
    
    # 4. 处理数据库异常
    elif isinstance(exc, SQLAlchemyError):
        error_details = {
            "original_error": str(exc)
        }
        error_response = ErrorResponse(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="数据库操作失败",
            error_details=error_details,
            request_id=request_id
        )
        log_level = "error"
    
    # 5. 处理其他未知异常
    else:
        error_details = {
            "exception_type": type(exc).__name__,
            "original_error": str(exc)
        }
        error_response = ErrorResponse(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="服务器内部错误",
            error_details=error_details,
            request_id=request_id
        )
        log_level = "error"
    
    # 记录异常日志
    log_exception(request, exc, error_response, log_level)
    
    # 返回标准化错误响应
    return JSONResponse(
        status_code=error_response.code,
        content=error_response.dict()
    )


def log_exception(request: Request, exc: Exception, error_response: ErrorResponse, log_level: str):
    """记录异常日志"""
    log_data = {
        "request_id": error_response.request_id,
        "path": request.url.path,
        "method": request.method,
        "client_ip": request.client.host if request.client else "unknown",
        "code": error_response.code,
        "error_message": error_response.message,
        "error_details": error_response.error_details,
        "exception_type": type(exc).__name__
    }
    
    # 根据日志级别记录日志
    if log_level == "debug":
        logger.debug(f"[Exception] {error_response.message}", extra=log_data)
    elif log_level == "info":
        logger.info(f"[Exception] {error_response.message}", extra=log_data)
    elif log_level == "warning":
        logger.warning(f"[Exception] {error_response.message}", extra=log_data)
    elif log_level == "error":
        logger.error(f"[Exception] {error_response.message}", extra=log_data, exc_info=True)
    elif log_level == "critical":
        logger.critical(f"[Exception] {error_response.message}", extra=log_data, exc_info=True)
