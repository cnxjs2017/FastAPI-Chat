from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_db
from app.models.conversation import Conversation
from app.models.user import User
from app.schemas.conversation import ConversationCreate, ConversationRead, ConversationWithMessages
from app.services.auth import get_current_user

router = APIRouter()


@router.post("/conversations/", response_model=ConversationRead)
def create_conversation(
        conversation: ConversationCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """创建新对话"""
    db_conversation = Conversation(
        title=conversation.title,
        user_id=current_user.id
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


@router.get("/conversations/", response_model=list[ConversationRead])
def get_conversations(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """获取当前用户的所有对话"""
    conversations = db.query(Conversation).filter(Conversation.user_id == current_user.id).all()
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
def get_conversation(
        conversation_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """获取对话详情"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="对话未找到")
    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此对话")
    return conversation
