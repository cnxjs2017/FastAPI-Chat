import json
import requests
from sqlmodel import Session
from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException

from app.services.auth import get_current_user
from app.core.database import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageCreate, MessageRead

router = APIRouter()

# AI 服务的 URL
AI_API_URL = ""


def send_to_ai(messages: List[Dict[str, str]]) -> str:
    """向 AI 发送请求并获取响应"""
    payload = {
        "model": "/groups/ai4legal/home/u12302024/LLaMA-Factory/models/Qwen2.5-7B-Instruct/Qwen2___5-7B-Instruct",
        "messages": messages,
        # "temperature": 0.7,
        # "top_p": 0.8,
        # "max_tokens": 512,
        # "repetition_penalty": 1.05
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(AI_API_URL, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        # 提取 AI 的消息内容
        response_data = response.json()
        ai_message = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return ai_message
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return "抱歉，AI 服务暂时不可用。"


@router.post("/conversations/{conversation_id}/messages/", response_model=MessageRead)
def create_message(
        conversation_id: int,
        message: MessageCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """创建新消息"""
    # 检查对话是否存在
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="对话未找到")
    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此对话")

    # 保存用户消息
    user_message = Message(
        content=message.content,
        is_user=True,
        conversation_id=conversation_id
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # 获取上下文（历史消息）
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    context = [
        {"role": "user" if msg.is_user else "assistant", "content": msg.content}
        for msg in messages
    ]

    # 向 AI 发送请求
    ai_response = send_to_ai(context)

    # 保存 AI 的回复
    ai_message = Message(
        content=ai_response,
        is_user=False,
        conversation_id=conversation_id
    )
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)

    return ai_message


@router.get("/conversations/{conversation_id}/messages/", response_model=list[MessageRead])
def get_messages(
        conversation_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """获取对话的所有消息"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="对话未找到")
    if conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此对话")

    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    return messages
