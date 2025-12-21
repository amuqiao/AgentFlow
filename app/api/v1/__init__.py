from fastapi import APIRouter
from app.api.v1 import auth, users, graphrag

# 创建API v1路由
api_v1_router = APIRouter()

# 包含认证路由
api_v1_router.include_router(auth.router, prefix="/auth", tags=["认证"])

# 包含用户路由
api_v1_router.include_router(users.router, prefix="/users", tags=["用户"])

# 包含GraphRAG路由
api_v1_router.include_router(graphrag.api_router, prefix="/graphrag", tags=["GraphRAG"])
