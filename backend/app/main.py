from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.logger import logger
from fastapi.security import HTTPAuthorizationCredentials

from app.core.config import settings
from app.core.security import get_current_user_id, security_scheme
from app.db.database import Base, Database, engine
from app.schemas.job import CreateJobRequest, CreateJobResponse
from app.schemas.resume import CreateResumeResponse, ResumeUploadResponse
from app.schemas.user import CreateUserRequest, Token, UserResponse
from app.services.auth_service import AuthService
from app.services.job_service import JobService
from app.services.report_service import ReportService
from app.services.resume_service import ResumeService

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)
database = Database()
auth_service = AuthService()
resume_service = ResumeService()
job_service = JobService()
report_service = ReportService()


@app.post("/register", response_model=Token)
def register_user(user_data: CreateUserRequest):
    session = database.get_session()
    try:
        return auth_service.register(user_data, session=session)
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
    finally:
        session.close()


@app.post("/login", response_model=Token)
def login_user(user_data: CreateUserRequest):
    session = database.get_session()
    try:
        return auth_service.login(user_data, session=session)
    finally:
        session.close()


@app.get("/me", response_model=UserResponse)
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
):
    session = database.get_session()
    try:
        user_id = get_current_user_id(credentials, session)
        return auth_service.get_user(user_id, session=session)
    finally:
        session.close()


@app.post("/resume/upload", response_model=ResumeUploadResponse)
def upload_resume(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
):
    session = database.get_session()
    try:
        user_id = get_current_user_id(credentials, session)
        return resume_service.upload(user_id, file, session=session)
    finally:
        session.close()


@app.get("/resume", response_model=list[CreateResumeResponse])
def get_resume(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    session = database.get_session()
    try:
        user_id = get_current_user_id(credentials, session)
        return resume_service.list_for_user(user_id, session=session)
    finally:
        session.close()


@app.get("/resume/{resume_id}", response_model=CreateResumeResponse)
def get_resume_by_id(
    resume_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    session = database.get_session()
    try:
        user_id = get_current_user_id(credentials, session)
        return resume_service.get_by_id(resume_id, user_id, session=session)
    finally:
        session.close()


@app.post("/job", response_model=CreateJobResponse)
def create_job(job_data: CreateJobRequest):
    session = database.get_session()
    try:
        return job_service.create(job_data, session=session)
    finally:
        session.close()


@app.get("/jobs", response_model=list[CreateJobResponse])
def get_jobs():
    session = database.get_session()
    try:
        return job_service.list_all(session=session)
    finally:
        session.close()


@app.get("/reports")
def get_reports(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    session = database.get_session()
    try:
        user_id = get_current_user_id(credentials, session)
        return report_service.list_for_user(user_id, session=session)
    finally:
        session.close()
