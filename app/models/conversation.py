from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # 使用字符串表示 User 模型
    user: Optional["User"] = Relationship(back_populates="conversations")

    # 使用字符串表示 Message 模型
    messages: List["Message"] = Relationship(back_populates="conversation")
