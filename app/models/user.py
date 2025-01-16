from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # 使用字符串表示 Conversation 模型
    conversations: List["Conversation"] = Relationship(back_populates="user")
