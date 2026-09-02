import argparse
import getpass

from app.core.security import hash_password
from app.database.session import SessionLocal
from app.repositories.admin import create_admin, get_admin_by_username


def main() -> None:
    parser = argparse.ArgumentParser(description="Create the initial school admin.")
    parser.add_argument("--username", required=True)
    args = parser.parse_args()
    password = getpass.getpass("Admin password: ")
    confirmation = getpass.getpass("Confirm password: ")
    if password != confirmation:
        parser.error("Passwords do not match.")
    if not password:
        parser.error("Password cannot be empty.")

    db = SessionLocal()
    try:
        if get_admin_by_username(db, args.username):
            parser.error("That username already exists.")
        create_admin(db, args.username, hash_password(password))
    finally:
        db.close()
    print(f"Created admin '{args.username}'.")


if __name__ == "__main__":
    main()
