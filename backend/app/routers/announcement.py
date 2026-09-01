from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.announcement import (
    create_announcement,
    delete_announcement,
    get_announcement,
    get_announcements,
    update_announcement,
)
from app.schemas.announcement import (
    AnnouncementCreate,
    AnnouncementResponse,
    AnnouncementUpdate,
)

router = APIRouter(prefix="/api", tags=["announcement"])


@router.get(
    "/announcements",
    response_model=list[AnnouncementResponse],
    summary="List announcements",
    description="Retrieve all announcements ordered by newest first.",
)
async def list_announcements(db: Session = Depends(get_db)) -> list[AnnouncementResponse]:
    """List all announcements."""
    return get_announcements(db)


@router.get(
    "/announcements/{announcement_id}",
    response_model=AnnouncementResponse,
    summary="Get announcement",
    description="Retrieve a single announcement by ID.",
)
async def get_announcement_endpoint(
    announcement_id: int, db: Session = Depends(get_db)
) -> AnnouncementResponse:
    """Get an announcement by ID."""
    announcement = get_announcement(db, announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return announcement


@router.post(
    "/announcements",
    response_model=AnnouncementResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create announcement",
    description="Create a new announcement.",
)
async def create_announcement_endpoint(
    announcement_data: AnnouncementCreate,
    db: Session = Depends(get_db),
) -> AnnouncementResponse:
    """Create a new announcement."""
    announcement = create_announcement(db, announcement_data.model_dump())
    return announcement


@router.put(
    "/announcements/{announcement_id}",
    response_model=AnnouncementResponse,
    summary="Update announcement",
    description="Update an announcement by ID.",
)
async def update_announcement_endpoint(
    announcement_id: int,
    announcement_data: AnnouncementUpdate,
    db: Session = Depends(get_db),
) -> AnnouncementResponse:
    """Update an announcement by ID."""
    announcement = get_announcement(db, announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    update_dict = {
        k: v for k, v in announcement_data.model_dump().items() if v is not None
    }
    if not update_dict:
        return announcement

    announcement = update_announcement(db, announcement, update_dict)
    return announcement


@router.delete(
    "/announcements/{announcement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete announcement",
    description="Delete an announcement by ID.",
)
async def delete_announcement_endpoint(
    announcement_id: int, db: Session = Depends(get_db)
) -> None:
    """Delete an announcement by ID."""
    announcement = get_announcement(db, announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    delete_announcement(db, announcement)
