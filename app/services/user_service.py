from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.password import get_password_hash, verify_password
from app.utils.jwt import create_access_token
from app.config.logger import logger
from app.repositories.sqlite.user_repository import UserRepository
from app.exception import BusinessException, AuthException, NotFoundException


class UserService:
    """用户服务类"""

    def __init__(self):
        self.user_repository = None

    def register_user(self, db: Session, user_create: UserCreate) -> User:
        """用户注册"""
        # 初始化仓储
        self.user_repository = UserRepository(db)

        # 检查用户名是否已存在
        existing_user = self.user_repository.get_by_username(user_create.username)
        if existing_user:
            logger.warning(
                f"User registration failed: username {user_create.username} already exists"
            )
            raise BusinessException(message="Username already registered", code=409)

        # 检查邮箱是否已存在
        existing_email = self.user_repository.get_by_email(user_create.email)
        if existing_email:
            logger.warning(
                f"User registration failed: email {user_create.email} already exists"
            )
            raise BusinessException(message="Email already registered", code=409)

        # 创建新用户
        hashed_password = get_password_hash(user_create.password)
        # 创建用户字典，排除password字段，使用password_hash
        user_data = user_create.dict(exclude={"password"})
        user_data["password_hash"] = hashed_password
        # 直接使用字典创建用户
        db_user = self.user_repository.create(user_data)

        logger.info(f"User registered successfully: {user_create.username}")
        return db_user

    def authenticate_user(self, db: Session, username: str, password: str) -> User:
        """用户认证"""
        # 初始化仓储
        self.user_repository = UserRepository(db)

        # 查询用户
        user = self.user_repository.get_by_username(username)
        if not user:
            logger.warning(f"Authentication failed: user {username} not found")
            raise AuthException(message="Incorrect username or password")

        # 验证密码
        if not verify_password(password, user.password_hash):
            logger.warning(
                f"Authentication failed: incorrect password for user {username}"
            )
            raise AuthException(message="Incorrect username or password")

        logger.info(f"User authenticated successfully: {username}")
        return user

    def get_user_by_id(self, db: Session, user_id: int) -> User:
        """根据ID获取用户"""
        # 初始化仓储
        self.user_repository = UserRepository(db)

        user = self.user_repository.get(user_id)
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise NotFoundException(message="User not found")
        return user

    @staticmethod
    def generate_token(user: User) -> str:
        """生成JWT令牌"""
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username}
        )
        logger.info(f"Generated access token for user: {user.username}")
        return access_token
