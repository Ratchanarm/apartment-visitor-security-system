from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.emergency_alert import AlertType, AlertPriority


class EmergencyAlertCreate(BaseModel):
    alert_type: AlertType
    priority: AlertPriority = AlertPriority.MEDIUM
    title: str
    description: Optional[str] = None
    location: Optional[str] = None


class EmergencyAlertResponse(BaseModel):
    id: int
    resident_id: Optional[int]
    guard_id: Optional[int]
    alert_type: AlertType
    priority: AlertPriority
    title: str
    description: Optional[str]
    location: Optional[str]
    is_resolved: bool
    resolved_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
