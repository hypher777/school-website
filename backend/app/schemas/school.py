from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SchoolBase(BaseModel):
    """Base school schema with common fields."""

    name: str = Field(..., min_length=1, max_length=200, description="School name")
    description: str | None = Field(
        None, max_length=5000, description="School description"
    )
    address: str | None = Field(
        None, max_length=500, description="School address"
    )
    phone: str | None = Field(None, max_length=30, description="School phone number")
    email: str | None = Field(None, max_length=255, description="School email")
    logo_url: str | None = Field(
        None, max_length=500, description="School logo URL"
    )
    established_year: int | None = Field(
        None, ge=1800, le=2100, description="Year school was established"
    )


class SchoolCreate(SchoolBase):
    """Schema for creating a school."""

    pass


class SchoolUpdate(BaseModel):
    """Schema for updating a school.

    All fields are optional so partial updates are supported.
    """

    name: str | None = Field(
        None, min_length=1, max_length=200, description="School name"
    )
    description: str | None = Field(
        None, max_length=5000, description="School description"
    )
    address: str | None = Field(
        None, max_length=500, description="School address"
    )
    phone: str | None = Field(None, max_length=30, description="School phone number")
    email: str | None = Field(None, max_length=255, description="School email")
    logo_url: str | None = Field(
        None, max_length=500, description="School logo URL"
    )
    established_year: int | None = Field(
        None, ge=1800, le=2100, description="Year school was established"
    )


class SchoolResponse(SchoolBase):
    """Schema for school responses with metadata."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
