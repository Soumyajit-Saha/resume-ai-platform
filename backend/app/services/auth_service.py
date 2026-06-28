from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import CreateUserRequest, Token, UserResponse



class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register(self, user_data: CreateUserRequest, session: Session) -> Token:
        if self.user_repo.get_by_email(user_data.email, session=session):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        hashed_password = get_password_hash(user_data.password)
        user = self.user_repo.create(str(user_data.email), hashed_password, session=session)
        token = create_access_token(str(user.id), timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        return Token(access_token=token)

    def login(self, user_data: CreateUserRequest, session: Session):
        user = self.user_repo.get_by_email(user_data.email, session=session)
        if not user or not verify_password(user_data.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = create_access_token(str(user.id), timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        return Token(access_token=token)

    def get_user(self, user_id: int, session: Session):
        user = self.user_repo.get_by_id(user_id, session=session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse.model_validate(user)
