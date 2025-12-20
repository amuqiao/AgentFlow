from fastapi import FastAPI, Depends, Request
import argparse
import os
from app.dependencies.config import (
    app_settings,
    config_deps,
    AppSettings,
    SQLiteConfig,
    LoggingConfig,
)
from app.dependencies.db import database_manager, sqlite
from app.api.v1 import api_v1_router
from app.middleware import setup_cors, request_logger_middleware
from app.middleware.request import request_id_middleware
from app.exception import custom_exception_handler
from app.exception.base import BaseAppException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.config.logger import logger

# 创建FastAPI应用
app = FastAPI(
    title=app_settings.APP_NAME,
    version=app_settings.APP_VERSION,
    openapi_url=f"{app_settings.API_V1_STR}/openapi.json",
)


# 应用启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动事件 - 初始化数据库连接"""
    logger.info(f"应用启动: {app_settings.APP_NAME} v{app_settings.APP_VERSION}")
    logger.info("正在连接所有数据库...")
    database_manager.connect_all()
    # 创建所有表
    sqlite.Base.metadata.create_all(bind=sqlite.engine)
    logger.info("所有数据库连接成功")


# 应用关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件 - 断开数据库连接"""
    logger.info("应用关闭，正在断开数据库连接...")
    database_manager.disconnect_all()
    logger.info("所有数据库连接已断开")


# 设置CORS中间件
setup_cors(app)

# 添加请求日志中间件
app.middleware("http")(request_logger_middleware)

# 添加Request ID中间件
app.middleware("http")(request_id_middleware)


# 注册全局异常处理器
app.add_exception_handler(BaseAppException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, custom_exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_exception_handler)
app.add_exception_handler(Exception, custom_exception_handler)


# 包含API v1路由
app.include_router(api_v1_router, prefix=app_settings.API_V1_STR)


@app.get("/")
def root():
    """根路径"""
    return {
        "message": "Welcome to FastAPI Enterprise Architecture",
        "version": app_settings.APP_VERSION,
        "api_v1": app_settings.API_V1_STR,
    }


@app.get("/api/v1/config")
def get_config(
    app_config: AppSettings = config_deps.app(),
    db_config: SQLiteConfig = config_deps.sqlite(),
    log_config: LoggingConfig = config_deps.logging(),
):
    """测试配置依赖注入"""
    return {
        "app_name": app_config.APP_NAME,
        "environment": app_config.ENVIRONMENT,
        "sqlite_url": db_config.URL,
        "log_level": log_config.LEVEL,
        "log_file": log_config.FILE,
    }


if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description="Agent Service API Server",
        epilog="""
使用示例：

1. 默认方式运行（开启热重载）：
   python main.py

2. 关闭热重载模式运行：
   python main.py --no-reload

3. 指定主机和端口运行：
   python main.py --host 127.0.0.1 --port 8080

4. 使用环境变量配置：
   export UVICORN_RELOAD=false UVICORN_HOST=127.0.0.1 UVICORN_PORT=8080
   python main.py

5. 查看帮助信息：
   python main.py -h
   """,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # 添加reload参数
    parser.add_argument(
        "--reload",
        action="store_true",
        default=os.getenv("UVICORN_RELOAD", "true").lower() == "true",
        help="Enable hot reload mode (default: true)",
    )

    # 添加host参数
    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("UVICORN_HOST", "0.0.0.0"),
        help="Host to bind (default: 0.0.0.0)",
    )

    # 添加port参数
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("UVICORN_PORT", "8000")),
        help="Port to bind (default: 8001)",
    )

    # 解析命令行参数
    args = parser.parse_args()

    # 显示API文档访问地址
    # 如果是本地服务器，使用localhost而不是0.0.0.0或127.0.0.1
    display_host = args.host
    if args.host in ("0.0.0.0", "127.0.0.1"):
        display_host = "localhost"

    print("\nAgent Service API Server 已启动")
    print("=====================================")
    print(f"服务地址: http://{args.host}:{args.port}")
    print(f"Swagger UI: http://{display_host}:{args.port}/docs")
    print(f"ReDoc: http://{display_host}:{args.port}/redoc")
    print("=====================================")
    print("按 Ctrl+C 停止服务\n")

    # 运行uvicorn服务器
    import uvicorn

    logger.info(f"Starting {app_settings.APP_NAME} v{app_settings.APP_VERSION}")
    if args.reload:
        # 当启用reload模式时，需要使用导入字符串
        uvicorn.run("main:app", host=args.host, port=args.port, reload=True)
    else:
        # 非reload模式可以直接传递应用对象
        uvicorn.run(app, host=args.host, port=args.port, reload=False)
