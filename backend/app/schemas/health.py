from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    app: str
    database: str = "ok"
