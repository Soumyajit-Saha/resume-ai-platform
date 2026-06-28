from sqlalchemy.orm import Session
from typing import List

from app.models.resume import Resume


class ResumeRepository:

    def create(self, user_id: int, filename: str, filepath: str, session: Session, status: str = "UPLOADED") -> Resume:
        resume = Resume(user_id=user_id, filename=filename, filepath=filepath, status=status)
        session.add(resume)
        session.commit()
        session.refresh(resume)
        return resume

    def list_by_user(self, user_id: int, session: Session) -> List[Resume]:
        return session.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).all()

    def get_by_id(self, resume_id: int, session: Session) -> Resume:
        return session.query(Resume).filter(Resume.id == resume_id).first()
