from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import db_session
from app.db.models import Job

router = APIRouter()


@router.get("/jobs")
def get_jobs(db: Session = Depends(db_session)):
    return db.query(Job).all()
