from fastapi import FastAPI

from app.core.configuration.settings import settings
from app.routers.health import router as health_router

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.debug,
)

app.include_router(health_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": settings.app_name, "status": "ready"}
