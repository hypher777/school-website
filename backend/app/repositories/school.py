from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.school import School


def get_school(db: Session) -> School | None:
    """Retrieve the first/only school from the database."""
    query = select(School)
    return db.scalars(query).first()


def count_schools(db: Session) -> int:
    """Count total number of schools in the database."""
    query = select(School)
    return len(db.scalars(query).all())


def create_school(db: Session, school_data: dict) -> School:
    """Create a new school record."""
    school = School(**school_data)
    db.add(school)
    db.commit()
    db.refresh(school)
    return school


def update_school(db: Session, school: School, school_data: dict) -> School:
    """Update an existing school record."""
    for key, value in school_data.items():
        if value is not None:
            setattr(school, key, value)
    db.add(school)
    db.commit()
    db.refresh(school)
    return school


def delete_school(db: Session, school: School) -> None:
    """Delete a school record."""
    db.delete(school)
    db.commit()
