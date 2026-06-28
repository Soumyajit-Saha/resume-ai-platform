from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def get_by_email(self, email: str, session: Session) -> User:
        return session.query(User).filter(User.email == email).first()

    def create(self, email: str, password_hash: str, session: Session) -> User:
        user = User(email=email, password_hash=password_hash)
        session.add(user)
        session.flush()
        session.commit()
        session.refresh(user)
        return user

    def get_by_id(self, user_id: int, session: Session) -> User:
        return session.query(User).filter(User.id == user_id).first()
