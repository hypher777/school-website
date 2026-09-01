from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AnnouncementBase(BaseModel):
    """Base announcement schema with common fields."""

    title: str = Field(..., min_length=1, max_length=200, description="Announcement title")
    content: str = Field(..., min_length=1, description="Announcement content")
    published: bool = Field(default=False, description="Whether the announcement is published")


class AnnouncementCreate(AnnouncementBase):
    """Schema for creating an announcement."""

    pass


class AnnouncementUpdate(BaseModel):
    """Schema for updating an announcement.

    All fields are optional so partial updates are supported.
    """

    title: str | None = Field(
        None, min_length=1, max_length=200, description="Announcement title"
    )
    content: str | None = Field(
        None, min_length=1, description="Announcement content"
    )
    published: bool | None = Field(
        None, description="Whether the announcement is published"
    )


class AnnouncementResponse(AnnouncementBase):
    """Schema for announcement responses with metadata."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
