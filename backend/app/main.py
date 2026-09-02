import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.core.configuration.settings import settings
from app.routers.announcement import router as announcement_router
from app.routers.auth import router as auth_router
from app.routers.event import router as event_router
from app.routers.health import router as health_router
from app.routers.school import router as school_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("school_api")

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
    description="School Website Backend API",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts_list)


@app.middleware("http")
async def log_requests(request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - started) * 1000
    logger.info("%s %s %s %.1fms", request.method, request.url.path, response.status_code, elapsed_ms)
    return response

# Include routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(school_router)
app.include_router(announcement_router)
app.include_router(event_router)


@app.get(
    "/",
    summary="Root endpoint",
    description="Returns application information.",
)
async def root() -> dict[str, str]:
    return {"message": settings.app_name, "status": "ready"}
