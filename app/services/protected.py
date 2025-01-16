from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.core.database import get_db
from app.core.security import decode_access_token, is_token_blacklisted
from app.models.user import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """获取当前用户"""
    # 检查令牌是否在黑名单中
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="令牌已失效")

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的令牌")
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")
    return user


@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    """受保护的路由"""
    return {"message": f"你好, {current_user.username}!"}
