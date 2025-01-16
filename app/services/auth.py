from sqlmodel import Session

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token, add_to_blacklist, \
    decode_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserLogin

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 创建新用户
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    # 检查用户是否存在
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    # 生成 JWT 令牌
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    """用户注销"""
    # 将当前令牌加入黑名单
    add_to_blacklist(token)
    return {"message": "注销成功"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """从 JWT 令牌中获取当前用户"""
    # 解码 JWT 令牌
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的令牌")

    # 从令牌中提取用户名
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="无效的令牌")

    # 从数据库中查找用户
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    return user
