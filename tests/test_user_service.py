from app.services.user_service import UserService
from app.schemas.user import UserCreate
from app.exception import BusinessException, AuthException


def test_register_user(db):
    """测试用户注册功能"""
    # 创建用户注册数据
    user_data = UserCreate(
        username="newuser", email="new@example.com", password="newpassword"
    )

    # 测试用户注册
    user = UserService().register_user(db, user_data)

    # 验证用户创建成功
    assert user.username == "newuser"
    assert user.email == "new@example.com"
    assert user.id is not None


def test_register_existing_username(db):
    """测试注册已存在的用户名"""
    # 先创建一个用户
    user_data = UserCreate(
        username="existinguser", email="existing@example.com", password="password123"
    )
    UserService().register_user(db, user_data)

    # 尝试使用相同的用户名注册新用户
    duplicate_user_data = UserCreate(
        username="existinguser", email="different@example.com", password="password456"
    )

    # 验证抛出BusinessException异常
    try:
        UserService().register_user(db, duplicate_user_data)
        assert False, "Expected BusinessException was not raised"
    except BusinessException as e:
        assert e.message == "Username already registered"
        assert e.code == 409


def test_register_existing_email(db):
    """测试注册已存在的邮箱"""
    # 先创建一个用户
    user_data = UserCreate(
        username="user1", email="common@example.com", password="password123"
    )
    UserService().register_user(db, user_data)

    # 尝试使用相同的邮箱注册新用户
    duplicate_user_data = UserCreate(
        username="user2", email="common@example.com", password="password456"
    )

    # 验证抛出BusinessException异常
    try:
        UserService().register_user(db, duplicate_user_data)
        assert False, "Expected BusinessException was not raised"
    except BusinessException as e:
        assert e.message == "Email already registered"
        assert e.code == 409


def test_authenticate_user_success(db):
    """测试用户认证成功"""
    # 先创建一个用户
    user_data = UserCreate(
        username="authuser", email="auth@example.com", password="authpassword"
    )
    UserService().register_user(db, user_data)

    # 测试正确的用户名和密码认证
    user = UserService().authenticate_user(db, "authuser", "authpassword")

    # 验证认证成功
    assert user is not None
    assert user.username == "authuser"


def test_authenticate_user_invalid_username(db):
    """测试使用无效用户名认证"""
    # 测试使用不存在的用户名认证
    try:
        UserService().authenticate_user(db, "nonexistent", "password123")
        assert False, "Expected AuthException was not raised"
    except AuthException as e:
        assert e.message == "Incorrect username or password"
        assert e.code == 401


def test_authenticate_user_invalid_password(db):
    """测试使用无效密码认证"""
    # 先创建一个用户
    user_data = UserCreate(
        username="authuser2", email="auth2@example.com", password="correctpassword"
    )
    UserService().register_user(db, user_data)

    # 测试使用错误的密码认证
    try:
        UserService().authenticate_user(db, "authuser2", "wrongpassword")
        assert False, "Expected AuthException was not raised"
    except AuthException as e:
        assert e.message == "Incorrect username or password"
        assert e.code == 401
