from fastapi import APIRouter

from app.api.routes import chatbot, login, threads, users, utils

api_router = APIRouter()
api_router.include_router(chatbot.router)
api_router.include_router(threads.router)
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
