from pydantic import BaseModel


class CreateJobRequest(BaseModel):
    title: str
    company: str
    description: str


class CreateJobResponse(BaseModel):
    id: int
    title: str
    company: str
    description: str

    class Config:
        from_attributes = True
