from sqlalchemy.orm import Session

from app.models.job import Job


class JobRepository:

    def create(self, title: str, company: str, description: str, session: Session) -> Job:
        job = Job(title=title, company=company, description=description)
        session.add(job)
        session.commit()
        session.refresh(job)
        return job

    def list_all(self, session: Session) -> list[Job]:
        return session.query(Job).order_by(Job.created_at.desc()).all()
