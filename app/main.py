from fastapi import FastAPI
from app.core.database import create_db_and_tables
from app.services.auth import router as auth_router
from app.services.protected import router as protected_router
from app.services.conversation import router as conversation_router
from app.services.message import router as message_router

app = FastAPI()

# 注册路由
app.include_router(auth_router, prefix="/auth")
app.include_router(protected_router, prefix="/services")
app.include_router(conversation_router, prefix="/services")
app.include_router(message_router, prefix="/services")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
