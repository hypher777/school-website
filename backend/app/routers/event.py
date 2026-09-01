from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.event import (
    create_event,
    delete_event,
    get_event,
    get_events,
    update_event,
)
from app.schemas.event import EventCreate, EventResponse, EventUpdate

router = APIRouter(prefix="/api", tags=["event"])


@router.get(
    "/events",
    response_model=list[EventResponse],
    summary="List events",
    description="Retrieve all events ordered by date.",
)
async def list_events(db: Session = Depends(get_db)) -> list[EventResponse]:
    """List all events."""
    return get_events(db)


@router.get(
    "/events/{event_id}",
    response_model=EventResponse,
    summary="Get event",
    description="Retrieve a single event by ID.",
)
async def get_event_endpoint(
    event_id: int, db: Session = Depends(get_db)
) -> EventResponse:
    """Get an event by ID."""
    event = get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post(
    "/events",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create event",
    description="Create a new event.",
)
async def create_event_endpoint(
    event_data: EventCreate,
    db: Session = Depends(get_db),
) -> EventResponse:
    """Create a new event."""
    event = create_event(db, event_data.model_dump())
    return event


@router.put(
    "/events/{event_id}",
    response_model=EventResponse,
    summary="Update event",
    description="Update an event by ID.",
)
async def update_event_endpoint(
    event_id: int,
    event_data: EventUpdate,
    db: Session = Depends(get_db),
) -> EventResponse:
    """Update an event by ID."""
    event = get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    update_dict = {
        k: v for k, v in event_data.model_dump().items() if v is not None
    }
    if not update_dict:
        return event

    event = update_event(db, event, update_dict)
    return event


@router.delete(
    "/events/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete event",
    description="Delete an event by ID.",
)
async def delete_event_endpoint(event_id: int, db: Session = Depends(get_db)) -> None:
    """Delete an event by ID."""
    event = get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    delete_event(db, event)
