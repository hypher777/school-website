from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.configuration.settings import settings
from app.routers.announcement import router as announcement_router
from app.routers.health import router as health_router
from app.routers.school import router as school_router

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
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(school_router)
app.include_router(announcement_router)


@app.get(
    "/",
    summary="Root endpoint",
    description="Returns application information.",
)
async def root() -> dict[str, str]:
    return {"message": settings.app_name, "status": "ready"}
