# 旧的认证依赖模块，已迁移到app.dependencies.auth
# 保留此文件用于向后兼容
from app.dependencies.auth import (
    get_current_user,
    oauth2_scheme,
    AuthDeps,
    auth_deps,
)

__all__ = [
    "get_current_user",
    "oauth2_scheme",
    "AuthDeps",
    "auth_deps",
]
