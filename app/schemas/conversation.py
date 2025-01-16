from pydantic import BaseModel
from datetime import datetime

from app.schemas.message import MessageRead


class ConversationBase(BaseModel):
    title: str


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: int
    user_id: int
    created_at: datetime


class ConversationWithMessages(ConversationRead):
    messages: list["MessageRead"]
