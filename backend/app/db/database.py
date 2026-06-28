from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Database:
    def __init__(self, engine=engine, SessionLocal=SessionLocal, Base=Base):
        self.engine = engine
        self.SessionLocal = SessionLocal
        self.Base = Base

    def get_session(self):
        return self.SessionLocal()
