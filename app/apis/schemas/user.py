from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    id: str
    password: str
    created_at: datetime
    updated_at: datetime

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
