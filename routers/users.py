from fastapi import APIRouter, Response, status, Depends
from pydantic import BaseModel, UUID4
from datetime import datetime
import uuid, json
from sqlalchemy.orm import Session

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

def sqlalchemy_to_dict(obj):
    data = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    if "id" in data and isinstance(data["id"], uuid.UUID):
        data["id"] = str(data["id"])
    return data

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()

@router.get("/users/", tags=["users"])
async def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    data = [sqlalchemy_to_dict(user) for user in users]
    res = Response(json.dumps({"data": data}))
    res.headers['Content-Type'] = 'application/json'
    return res