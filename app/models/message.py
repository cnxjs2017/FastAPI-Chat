from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    content: str
    is_user: bool = Field(default=True)  # 默认值为 True，表示用户消息
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # 使用字符串表示 Conversation 模型
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
