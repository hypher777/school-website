from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.configuration.settings import settings
from app.database.dependencies import get_db
from app.schemas.health import HealthResponse

router = APIRouter(prefix="/api", tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check application health.",
)
async def health_check(db: Session = Depends(get_db)) -> HealthResponse:
    """Check the health of the application.

    Returns 200 OK if the application is operational.
    Database connectivity is checked by the application's ability to respond.
    """
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable",
        ) from exc
    return HealthResponse(status="ok", app=settings.app_name, database="ok")
