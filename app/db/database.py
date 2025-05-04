from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

# from app.db.data import employers, job_applications, jobs, users
from app.db.models import Base  # Employer, Job, JobApplication, User
from app.settings.config import get_settings

settings = get_settings()

engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


def db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def prepare_database():
    # from app.gql.utils import hash_password

    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # session = Session()

    # for employer in employers:
    #     emp = Employer(**employer)
    #     session.add(emp)

    # for job in jobs:
    #     session.add(Job(**job))

    # for user in users:
    #     user["password_hash"] = hash_password(user["password"])
    #     del user["password"]
    #     session.add(User(**user))

    # for job_application in job_applications:
    #     session.add(JobApplication(**job_application))

    # session.commit()
    # session.close()
    print("Database prepared.")
