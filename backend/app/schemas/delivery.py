from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.delivery import DeliveryStatus


class DeliveryCreate(BaseModel):
    resident_id: int
    courier_name: Optional[str] = None
    courier_company: Optional[str] = None
    tracking_number: Optional[str] = None
    package_description: Optional[str] = None
    notes: Optional[str] = None


class DeliveryUpdate(BaseModel):
    status: Optional[DeliveryStatus] = None
    notes: Optional[str] = None


class DeliveryResponse(BaseModel):
    id: int
    resident_id: int
    courier_name: Optional[str]
    courier_company: Optional[str]
    tracking_number: Optional[str]
    package_description: Optional[str]
    photo_url: Optional[str]
    status: DeliveryStatus
    received_at: Optional[datetime]
    delivered_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
