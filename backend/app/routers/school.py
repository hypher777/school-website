from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.repositories.school import (
    count_schools,
    create_school,
    delete_school,
    get_school as get_school_repo,
    update_school,
)
from app.schemas.school import SchoolCreate, SchoolResponse, SchoolUpdate

router = APIRouter(prefix="/api", tags=["school"])


@router.get(
    "/school",
    response_model=SchoolResponse,
    summary="Get school information",
    description="Retrieve the school configuration and information.",
)
async def get_school(db: Session = Depends(get_db)) -> SchoolResponse:
    """Get the school information."""
    school = get_school_repo(db)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


@router.post(
    "/school",
    response_model=SchoolResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create school",
    description="Create the school configuration. Only one school allowed.",
)
async def create_school_endpoint(
    school_data: SchoolCreate,
    db: Session = Depends(get_db),
) -> SchoolResponse:
    """Create a new school record.

    Returns 409 Conflict if a school already exists.
    """
    if count_schools(db) > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A school already exists. Use PUT to update it.",
        )
    school = create_school(db, school_data.model_dump())
    return school


@router.put(
    "/school",
    response_model=SchoolResponse,
    summary="Update school",
    description="Update the school configuration.",
)
async def update_school_endpoint(
    school_data: SchoolUpdate,
    db: Session = Depends(get_db),
) -> SchoolResponse:
    """Update the school information.

    Returns 404 if the school does not exist.
    """
    school = get_school_repo(db)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    # Only update provided fields
    update_dict = {
        k: v for k, v in school_data.model_dump().items() if v is not None
    }
    if not update_dict:
        # No fields to update, just return existing
        return school

    school = update_school(db, school, update_dict)
    return school


@router.delete(
    "/school",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete school",
    description="Delete the school configuration.",
)
async def delete_school_endpoint(db: Session = Depends(get_db)) -> None:
    """Delete the school information.

    Returns 404 if the school does not exist.
    """
    school = get_school_repo(db)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    delete_school(db, school)
