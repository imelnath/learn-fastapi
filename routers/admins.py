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

@router.get("/admins/db", tags=["admins"], response_model=list[schemas.Admin])
async def read_admins_from_db(db: Session = Depends(get_db)):
    admins = db.query(models.Admin).all()
    return admins
    # return schemas.admin_list

@router.get("/admins/", tags=["admins"], response_model=list[schemas.Admin])
async def read_admins():
    return schemas.admin_list

@router.post("/admins/", tags=["admins"])
async def add_admin(admin: schemas.AdminIn):
    new_admin = schemas.Admin(
        id=uuid.uuid4(),
        username=admin.username,
        password=admin.password,
        lastLogin=datetime.now(),
        isSuperUser=admin.isSuperUser
    )
    schemas.admin_list.append(new_admin)
    return new_admin

@router.put("/admins/{id}", tags=["admins"])
async def edit_admmin(id: UUID4, admin: schemas.AdminIn):
    for _admin in schemas.admin_list:
        if _admin.id == id:
            _admin.username = admin.username
            _admin.password = admin.password
            _admin.isSuperUser =admin.isSuperUser
            return _admin

@router.delete("/admins/{id}", tags=["admins"])
async def delete_admin(id: UUID4):
    for index, admin in enumerate(schemas.admin_list):
        if admin.id == id:
            del schemas.admin_list[index]
            return {"message": "Admin deleted"}