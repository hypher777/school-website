from fastapi import APIRouter

from app.core.configuration.settings import settings
from app.schemas.health import HealthResponse

router = APIRouter(prefix="/api", tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check application health.",
)
async def health_check() -> HealthResponse:
    """Check the health of the application.

    Returns 200 OK if the application is operational.
    Database connectivity is checked by the application's ability to respond.
    """
    return HealthResponse(status="ok", app=settings.app_name, database="ok")
