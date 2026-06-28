from pathlib import Path
from typing import List

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR
from app.repositories.resume_repository import ResumeRepository
from app.schemas.resume import CreateResumeResponse, ResumeUploadResponse


class ResumeService:
    def __init__(self):
        self.resume_repo = ResumeRepository()

    def upload(self, user_id: int, file: UploadFile, session: Session) -> ResumeUploadResponse:
        filename = file.filename or "resume.pdf"
        saved_path = UPLOAD_DIR / filename
        with saved_path.open("wb") as handle:
            handle.write(file.file.read())

        resume = self.resume_repo.create(user_id=user_id, filename=filename, filepath=str(saved_path), session=session)
        return ResumeUploadResponse(resumeId=resume.id, status=resume.status)

    def list_for_user(self, user_id: int, session: Session) -> List[CreateResumeResponse]:
        resumes = self.resume_repo.list_by_user(user_id, session=session)
        return [CreateResumeResponse.model_validate(resume) for resume in resumes]

    def get_by_id(self, resume_id: int, user_id: int, session: Session) -> CreateResumeResponse:
        resume = self.resume_repo.get_by_id(resume_id, session=session)
        if not resume or resume.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
        return CreateResumeResponse.model_validate(resume)
