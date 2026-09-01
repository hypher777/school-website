from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventBase(BaseModel):
    """Base event schema with common fields."""

    title: str = Field(..., min_length=1, max_length=200, description="Event title")
    description: str | None = Field(
        None, max_length=5000, description="Event description"
    )
    event_date: datetime = Field(..., description="Date and time of the event")
    location: str | None = Field(None, max_length=255, description="Event location")
    published: bool = Field(default=False, description="Whether the event is published")


class EventCreate(EventBase):
    """Schema for creating an event."""

    pass


class EventUpdate(BaseModel):
    """Schema for updating an event.

    All fields are optional so partial updates are supported.
    """

    title: str | None = Field(
        None, min_length=1, max_length=200, description="Event title"
    )
    description: str | None = Field(
        None, max_length=5000, description="Event description"
    )
    event_date: datetime | None = Field(
        None, description="Date and time of the event"
    )
    location: str | None = Field(None, max_length=255, description="Event location")
    published: bool | None = Field(
        None, description="Whether the event is published"
    )


class EventResponse(EventBase):
    """Schema for event responses with metadata."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
