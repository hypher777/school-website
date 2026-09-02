from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.admin import Admin


def get_admin_by_username(db: Session, username: str) -> Admin | None:
    return db.scalars(select(Admin).where(Admin.username == username)).first()


def create_admin(db: Session, username: str, password_hash: str) -> Admin:
    admin = Admin(username=username, password_hash=password_hash)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
