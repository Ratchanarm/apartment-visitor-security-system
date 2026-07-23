from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.visitor import VisitorStatus


class VisitorCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    purpose: Optional[str] = None
    expected_arrival: Optional[datetime] = None
    expected_departure: Optional[datetime] = None
    notes: Optional[str] = None


class VisitorResponse(BaseModel):
    id: int
    resident_id: int
    name: str
    phone: Optional[str]
    email: Optional[str]
    purpose: Optional[str]
    expected_arrival: Optional[datetime]
    expected_departure: Optional[datetime]
    qr_code: Optional[str]
    status: VisitorStatus
    photo_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class VisitorCheckIn(BaseModel):
    qr_token: Optional[str] = None
    otp: Optional[str] = None
    photo_at_entry: Optional[str] = None
    notes: Optional[str] = None


class VisitorLogResponse(BaseModel):
    id: int
    visitor_id: int
    action: str
    timestamp: datetime
    notes: Optional[str]
    photo_at_entry: Optional[str]

    class Config:
        from_attributes = True
