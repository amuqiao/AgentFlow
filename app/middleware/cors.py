from fastapi.middleware.cors import CORSMiddleware
from app.dependencies.config import app_settings


def setup_cors(app):
    """设置CORS中间件"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.CORS_ORIGINS,
        allow_credentials=app_settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=app_settings.CORS_ALLOW_METHODS,
        allow_headers=app_settings.CORS_ALLOW_HEADERS,
    )
