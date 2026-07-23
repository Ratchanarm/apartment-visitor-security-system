from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.user import UserResponse
from app.schemas.apartment import ApartmentResponse


class ResidentCreate(BaseModel):
    user_id: int
    apartment_id: int
    is_owner: bool = False
    emergency_contact: Optional[str] = None


class ResidentResponse(BaseModel):
    id: int
    user: UserResponse
    apartment: ApartmentResponse
    is_owner: bool
    move_in_date: Optional[datetime]
    emergency_contact: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
