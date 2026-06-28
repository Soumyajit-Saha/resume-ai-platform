from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: int
    resume_id: int
    job_id: int
    status: str

    class Config:
        from_attributes = True
