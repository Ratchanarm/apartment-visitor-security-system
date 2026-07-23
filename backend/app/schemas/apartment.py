from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ApartmentCreate(BaseModel):
    building_name: str
    unit_number: str
    floor: Optional[int] = None
    block: Optional[str] = None
    address: Optional[str] = None


class ApartmentResponse(BaseModel):
    id: int
    building_name: str
    unit_number: str
    floor: Optional[int]
    block: Optional[str]
    address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
