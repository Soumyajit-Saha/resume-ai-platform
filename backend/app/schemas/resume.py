from pydantic import BaseModel


class CreateResumeResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    filepath: str
    status: str

    class Config:
        from_attributes = True


class ResumeUploadResponse(BaseModel):
    resumeId: int
    status: str
