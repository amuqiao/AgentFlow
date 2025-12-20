import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from app.databases.sqlite.connection import sqlite_connection

# 创建测试数据库引擎
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建测试会话工厂
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """创建测试数据库会话"""
    # 创建所有表
    sqlite_connection.Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # 测试结束后删除所有表
        sqlite_connection.Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """创建测试客户端"""

    def override_get_sqlite_db():
        try:
            yield db
        finally:
            db.close()

    # 只使用新的依赖项
    from app.dependencies.db import get_sqlite_db

    app.dependency_overrides[get_sqlite_db] = override_get_sqlite_db

    yield TestClient(app)

    # 恢复依赖项
    del app.dependency_overrides[get_sqlite_db]


@pytest.fixture(scope="function")
def test_user(db):
    """创建测试用户"""
    from app.models.user import User
    from app.utils.password import get_password_hash

    # 创建测试用户
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash("testpassword"),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture(scope="function")
def test_user_token(test_user, client):
    """获取测试用户的访问令牌"""
    # 登录获取令牌
    response = client.post(
        "/api/v1/auth/login", data={"username": "testuser", "password": "testpassword"}
    )

    return response.json()["access_token"]
