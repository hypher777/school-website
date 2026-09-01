from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event


def get_events(db: Session) -> list[Event]:
    """Retrieve all events ordered by upcoming date first."""
    query = select(Event).order_by(Event.event_date.desc(), Event.id.desc())
    return db.scalars(query).all()


def get_event(db: Session, event_id: int) -> Event | None:
    """Retrieve a single event by ID."""
    query = select(Event).where(Event.id == event_id)
    return db.scalars(query).first()


def create_event(db: Session, event_data: dict) -> Event:
    """Create a new event record."""
    event = Event(**event_data)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def update_event(db: Session, event: Event, event_data: dict) -> Event:
    """Update an existing event record."""
    for key, value in event_data.items():
        if value is not None:
            setattr(event, key, value)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def delete_event(db: Session, event: Event) -> None:
    """Delete an event record."""
    db.delete(event)
    db.commit()
