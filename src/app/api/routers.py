from fastapi import APIRouter
from app.api import ping, notes

api_router = APIRouter()

api_router.include_router(ping.router, prefix="/ping", tags=["ping"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
