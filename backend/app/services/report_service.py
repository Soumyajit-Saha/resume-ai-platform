from typing import List

from sqlalchemy.orm import Session

from app.repositories.report_repository import ReportRepository
from app.schemas.report import ReportResponse, ReportResponse


class ReportService:
    def __init__(self):
        self.report_repo = ReportRepository()

    def list_for_user(self, user_id: int, session: Session) -> List[ReportResponse]:
        reports = self.report_repo.list_by_user(user_id, session=session)
        return [ReportResponse.model_validate(report) for report in reports]
