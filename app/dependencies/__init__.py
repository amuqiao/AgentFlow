# FastAPI依赖注入模块
# 集中管理所有依赖注入，提供统一的导入入口

from typing import Any

__all__ = [
    # 配置依赖
    "get_app_settings",
    "get_sqlite_config", 
    "get_logging_config",
    # 数据库依赖
    "get_sqlite_db",
    # 认证依赖
    "get_current_user",
    "oauth2_scheme",
    # 服务层依赖
    "get_user_service",
    # 容器类
    "ConfigDeps",
    "DatabaseDeps",
    "AuthDeps",
    "ServiceDeps",
    # 快捷访问实例
    "config_deps",
    "db_deps",
    "auth_deps",
    "service_deps",
]

# 延迟导入依赖，避免循环导入问题
def __getattr__(name: str) -> Any:
    """动态导入依赖模块，解决循环导入问题"""
    if name in [
        "get_app_settings",
        "get_sqlite_config", 
        "get_logging_config",
        "ConfigDeps",
        "config_deps",
    ]:
        from app.dependencies.config import (
            ConfigDeps,
            config_deps,
            get_app_settings,
            get_sqlite_config,
            get_logging_config,
        )
        return locals()[name]
    elif name in [
        "get_sqlite_db",
        "DatabaseDeps",
        "db_deps",
    ]:
        from app.dependencies.db import (
            DatabaseDeps,
            db_deps,
            get_sqlite_db,
        )
        return locals()[name]
    elif name in [
        "get_current_user",
        "oauth2_scheme",
        "AuthDeps",
        "auth_deps",
    ]:
        from app.dependencies.auth import (
            AuthDeps,
            auth_deps,
            get_current_user,
            oauth2_scheme,
        )
        return locals()[name]
    elif name in [
        "get_user_service",
        "ServiceDeps",
        "service_deps",
    ]:
        from app.dependencies.service import (
            ServiceDeps,
            service_deps,
            get_user_service,
        )
        return locals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
