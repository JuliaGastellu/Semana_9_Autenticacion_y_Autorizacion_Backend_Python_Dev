import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.exceptions import register_exception_handlers
from app.middleware.request_logging import RequestLoggingMiddleware
from app.routers import auth, categories, comments, posts, users

logging.basicConfig(level=logging.INFO)
app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
register_exception_handlers(app)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/", tags=["health"])
async def health() -> dict[str, str]: return {"status": "ok", "service": settings.app_name}
