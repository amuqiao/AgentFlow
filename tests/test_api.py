def test_root_endpoint(client):
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to FastAPI Enterprise Architecture" in response.json()["message"]


def test_register_user(client):
    """测试用户注册API"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "apitestuser",
            "email": "apitest@example.com",
            "password": "apitestpassword",
        },
    )

    assert response.status_code == 201
    assert response.json()["username"] == "apitestuser"
    assert response.json()["email"] == "apitest@example.com"
    assert "id" in response.json()


def test_register_existing_user(client):
    """测试注册已存在的用户"""
    # 先注册一个用户
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "existingapiuser",
            "email": "existingapi@example.com",
            "password": "password123",
        },
    )

    # 尝试注册相同的用户名
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "existingapiuser",
            "email": "differentapi@example.com",
            "password": "password456",
        },
    )

    # 检查响应状态码和响应内容
    assert response.status_code == 409
    assert response.json()["code"] == 409
    assert response.json()["message"] == "Username already registered"


def test_login_success(client, test_user):
    """测试登录成功"""
    response = client.post(
        "/api/v1/auth/login", data={"username": "testuser", "password": "testpassword"}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """测试登录失败"""
    # 发送登录请求
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "invaliduser", "password": "invalidpassword"},
    )

    # 检查响应状态码和响应内容
    assert response.status_code == 401
    assert response.json()["code"] == 401
    assert response.json()["message"] == "Incorrect username or password"


def test_get_current_user(client, test_user_token):
    """测试获取当前用户信息"""
    response = client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"


def test_get_current_user_unauthorized(client):
    """测试未授权访问"""
    response = client.get("/api/v1/users/me")

    assert response.status_code == 401


def test_get_user_by_id(client, test_user, test_user_token):
    """测试根据ID获取用户信息"""
    response = client.get(
        f"/api/v1/users/{test_user.id}",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == test_user.id
    assert response.json()["username"] == test_user.username
