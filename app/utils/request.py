from fastapi import Request

REQUEST_ID_KEY = "request_id"

def set_request_id(request: Request, request_id: str):
    """设置Request ID到请求上下文"""
    if not hasattr(request.state, REQUEST_ID_KEY):
        setattr(request.state, REQUEST_ID_KEY, request_id)

def get_request_id(request: Request) -> str:
    """从请求上下文获取Request ID"""
    return getattr(request.state, REQUEST_ID_KEY, "")
