from sqlmodel import SQLModel, Session, create_engine

from app.core.config import settings

# 创建数据库引擎
engine = create_engine(settings.DATABASE_URL)


# 获取数据库会话
def get_db():
    with Session(engine) as session:
        yield session


# 创建数据库表
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
