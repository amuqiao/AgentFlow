import uuid
from fastapi import Request, Response
from app.utils.request import set_request_id

async def request_id_middleware(request: Request, call_next):
    """Request ID中间件"""
    # 从请求头获取Request ID，若不存在则生成新的
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    
    # 设置Request ID到请求上下文
    set_request_id(request, request_id)
    
    # 处理请求
    response = await call_next(request)
    
    # 将Request ID添加到响应头
    response.headers["X-Request-ID"] = request_id
    
    return response
