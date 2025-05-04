from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import db_session
from app.db.models import Employer

router = APIRouter()


@router.get("/employers")
def get_employers(db: Session = Depends(db_session)):
    return db.query(Employer).all()
