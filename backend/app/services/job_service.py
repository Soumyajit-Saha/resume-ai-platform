from typing import List

from sqlalchemy.orm import Session

from app.repositories.job_repository import JobRepository
from app.schemas.job import CreateJobRequest, CreateJobResponse


class JobService:
    def __init__(self):
        self.job_repo = JobRepository()

    def create(self, job_data: CreateJobRequest, session: Session) -> CreateJobResponse:
        job = self.job_repo.create(job_data.title, job_data.company, job_data.description, session=session)
        return CreateJobResponse.model_validate(job)

    def list_all(self, session: Session) -> List[CreateJobResponse]:
        jobs = self.job_repo.list_all(session=session)
        return [CreateJobResponse.model_validate(job) for job in jobs]
