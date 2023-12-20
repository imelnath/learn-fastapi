from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, UUID4
from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from auth import verify_token
from database import SessionLocal, engine
import models, schemas

router = APIRouter()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()

@router.get("/users/", tags=["users"], response_model=list[schemas.User])
async def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users