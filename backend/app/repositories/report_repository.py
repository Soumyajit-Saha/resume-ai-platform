from sqlalchemy.orm import Session

from app.models.report import Report
from app.models.resume import Resume


class ReportRepository:

    def create(self, resume_id: int, content: str, session: Session, status: str = "PENDING") -> Report:
        report = Report(resume_id=resume_id, content=content, status=status)
        session.add(report)
        session.commit()
        session.refresh(report)
        return report

    def list_by_user(self, user_id: int, session: Session) -> list[Report]:
        return session.query(Report).join(Resume, Report.resume_id == Resume.id).filter(Resume.user_id == user_id).all()
