from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, full_name: str, email: str, password: str, role: str = "employee") -> User:
    user = User(full_name=full_name, email=email, hashed_password=hash_password(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
