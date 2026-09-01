from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.announcement import Announcement


def get_announcements(db: Session) -> list[Announcement]:
    """Retrieve all announcements ordered by newest first."""
    query = select(Announcement).order_by(
        Announcement.created_at.desc(), Announcement.id.desc()
    )
    return db.scalars(query).all()


def get_announcement(db: Session, announcement_id: int) -> Announcement | None:
    """Retrieve a single announcement by ID."""
    query = select(Announcement).where(Announcement.id == announcement_id)
    return db.scalars(query).first()


def create_announcement(db: Session, announcement_data: dict) -> Announcement:
    """Create a new announcement record."""
    announcement = Announcement(**announcement_data)
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    return announcement


def update_announcement(
    db: Session, announcement: Announcement, announcement_data: dict
) -> Announcement:
    """Update an existing announcement record."""
    for key, value in announcement_data.items():
        if value is not None:
            setattr(announcement, key, value)
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    return announcement


def delete_announcement(db: Session, announcement: Announcement) -> None:
    """Delete an announcement record."""
    db.delete(announcement)
    db.commit()
