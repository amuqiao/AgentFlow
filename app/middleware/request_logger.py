import time
from fastapi import Request
from app.config.logger import logger


async def request_logger_middleware(request: Request, call_next):
    """请求日志中间件"""
    # 记录请求开始时间
    start_time = time.time()

    # 获取请求信息
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    url = str(request.url)
    headers = dict(request.headers)

    # 记录请求开始
    logger.info(f"Request started: {method} {url} from {client_ip}")
    logger.debug(f"Request headers: {headers}")

    # 处理请求
    response = await call_next(request)

    # 计算请求处理时间
    process_time = time.time() - start_time

    # 记录响应信息
    logger.info(
        f"Request completed: {method} {url} - Status: {response.status_code} - Time: {process_time:.3f}s"
    )

    return response
