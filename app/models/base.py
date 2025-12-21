# 通用模型基类，不直接依赖任何特定数据库
from sqlalchemy.ext.declarative import declarative_base

# 创建一个通用的Base类，用于所有数据模型
Base = declarative_base()
