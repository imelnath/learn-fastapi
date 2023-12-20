from pydantic import BaseModel, UUID4
from datetime import datetime
import uuid

class AdminIn(BaseModel):
    username: str
    password: str
    isSuperUser: bool   

    class Config:
        from_attributes = True

class Admin(AdminIn):
    id: UUID4
    lastLogin: datetime

class User(BaseModel):
    id: UUID4
    nama: str
    telp: str 

    class Config:
        from_attributes = True

admin_list: list[Admin] = [
    Admin(
        id=uuid.uuid4(),
        username="admin1",
        password="password1",
        lastLogin=datetime.now(),
        isSuperUser=True
    ),
    Admin(
        id=uuid.uuid4(),
        username="admin2",
        password="password2",
        lastLogin=datetime.now(),
        isSuperUser=False
    ),
]