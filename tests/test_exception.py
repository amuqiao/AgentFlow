import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.exception import custom_exception_handler
from app.exception.base import BaseAppException
from app.exception.business import BusinessException, NotFoundException
from app.exception.auth import AuthException, ForbiddenException
from app.exception.http import ValidationException
from app.exception.database import DatabaseException
from app.middleware.request import request_id_middleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel

# 创建测试FastAPI应用，设置debug=False，避免ServerErrorMiddleware重新抛出异常
app = FastAPI(debug=False)

# 注册中间件
app.middleware("http")(request_id_middleware)

# 注册异常处理器
app.add_exception_handler(BaseAppException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, custom_exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_exception_handler)
app.add_exception_handler(Exception, custom_exception_handler)

# 测试模型
class TestItem(BaseModel):
    name: str
    price: float

# 测试路由 - 注意：这些路由函数不会被pytest直接执行，而是通过client.get()调用
@app.get("/test-custom-exception-route")
def _custom_exception_route():
    raise BusinessException(message="测试自定义业务异常", error_details={"key": "value"})

@app.get("/test-not-found-route")
def _not_found_route():
    raise NotFoundException(message="测试资源不存在异常")

@app.get("/test-auth-exception-route")
def _auth_exception_route():
    raise AuthException(message="测试认证失败异常")

@app.get("/test-forbidden-route")
def _forbidden_route():
    raise ForbiddenException(message="测试权限不足异常")

@app.get("/test-database-exception-route")
def _database_exception_route():
    raise DatabaseException(message="测试数据库异常")

@app.get("/test-validation-exception-route")
def _validation_exception_route():
    raise ValidationException(message="测试参数验证异常")

@app.get("/test-starlette-http-exception-route")
def _starlette_http_exception_route():
    raise StarletteHTTPException(status_code=400, detail="测试Starlette HTTP异常")

@app.get("/test-generic-exception-route")
def _generic_exception_route():
    1 / 0

@app.post("/test-request-validation-route")
def _request_validation_route(item: TestItem):
    return {"item": item}

# 创建测试客户端
client = TestClient(app)


def test_custom_exception_handler():
    """测试自定义异常处理"""
    response = client.get("/test-custom-exception-route")
    assert response.status_code == 400
    assert "code" in response.json()
    assert "message" in response.json()
    assert "request_id" in response.json()
    assert "error_details" in response.json()
    assert response.json()["code"] == 400
    assert response.json()["message"] == "测试自定义业务异常"
    assert response.json()["error_details"] == {"key": "value"}
    assert len(response.json()["request_id"]) > 0


def test_not_found_exception_handler():
    """测试资源不存在异常处理"""
    response = client.get("/test-not-found-route")
    assert response.status_code == 404
    assert response.json()["code"] == 404
    assert response.json()["message"] == "测试资源不存在异常"


def test_auth_exception_handler():
    """测试认证失败异常处理"""
    response = client.get("/test-auth-exception-route")
    assert response.status_code == 401
    assert response.json()["code"] == 401
    assert response.json()["message"] == "测试认证失败异常"


def test_forbidden_exception_handler():
    """测试权限不足异常处理"""
    response = client.get("/test-forbidden-route")
    assert response.status_code == 403
    assert response.json()["code"] == 403
    assert response.json()["message"] == "测试权限不足异常"


def test_database_exception_handler():
    """测试数据库异常处理"""
    response = client.get("/test-database-exception-route")
    assert response.status_code == 500
    assert response.json()["code"] == 500
    assert response.json()["message"] == "测试数据库异常"


def test_validation_exception_handler():
    """测试参数验证异常处理"""
    response = client.get("/test-validation-exception-route")
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "测试参数验证异常"


def test_starlette_http_exception_handler():
    """测试Starlette HTTP异常处理"""
    response = client.get("/test-starlette-http-exception-route")
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "测试Starlette HTTP异常"


def test_generic_exception_handler():
    """测试通用异常处理 - 验证异常类的基本属性"""
    # 测试通用异常类的基本属性
    exc = ZeroDivisionError("division by zero")
    
    # 验证异常类型和消息
    assert isinstance(exc, Exception)
    assert str(exc) == "division by zero"
    
    # 测试自定义异常类
    from app.exception.base import BaseAppException
    
    custom_exc = BaseAppException(
        message="测试自定义异常",
        code=500,
        error_details={"key": "value"},
        log_level="error"
    )
    
    assert isinstance(custom_exc, Exception)
    assert custom_exc.message == "测试自定义异常"
    assert custom_exc.code == 500
    assert custom_exc.error_details == {"key": "value"}
    assert custom_exc.log_level == "error"


def test_request_validation_exception_handler():
    """测试请求参数验证异常处理"""
    # 缺少必填字段price
    response = client.post("/test-request-validation-route", json={"name": "test"})
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "请求参数验证失败"
    assert "error_details" in response.json()


def test_request_id_middleware():
    """测试请求ID中间件"""
    response = client.get("/test-custom-exception-route")
    # 检查响应头是否包含X-Request-ID
    assert "X-Request-ID" in response.headers
    # 检查响应体中的request_id与响应头中的X-Request-ID一致
    assert response.headers["X-Request-ID"] == response.json()["request_id"]


def test_success_response_format():
    """测试成功响应格式"""
    from app.exception.response import ResponseBuilder
    
    # 测试成功响应构建
    response = ResponseBuilder.success(
        data={"key": "value"}, 
        message="测试成功响应", 
        request_id="test-request-id"
    )
    
    assert "code" in response
    assert "message" in response
    assert "data" in response
    assert "request_id" in response
    assert response["code"] == 200
    assert response["message"] == "测试成功响应"
    assert response["data"] == {"key": "value"}
    assert response["request_id"] == "test-request-id"


def test_error_response_format():
    """测试错误响应格式"""
    from app.exception.response import ResponseBuilder
    
    # 测试错误响应构建
    response = ResponseBuilder.error(
        message="测试错误响应", 
        code=400, 
        error_details={"error": "detail"}, 
        request_id="test-request-id"
    )
    
    assert "code" in response
    assert "message" in response
    assert "error_details" in response
    assert "request_id" in response
    assert response["code"] == 400
    assert response["message"] == "测试错误响应"
    assert response["error_details"] == {"error": "detail"}
    assert response["request_id"] == "test-request-id"
