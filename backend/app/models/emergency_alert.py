from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum as SQLEnum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class AlertType(str, enum.Enum):
    FIRE = "fire"
    MEDICAL = "medical"
    SECURITY = "security"
    MAINTENANCE = "maintenance"
    OTHER = "other"


class AlertPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EmergencyAlert(Base):
    __tablename__ = "emergency_alerts"

    id = Column(Integer, primary_key=True, index=True)
    resident_id = Column(Integer, ForeignKey("residents.id"))
    guard_id = Column(Integer, ForeignKey("security_guards.id"))
    alert_type = Column(SQLEnum(AlertType), nullable=False)
    priority = Column(SQLEnum(AlertPriority), default=AlertPriority.MEDIUM)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    location = Column(String(200))
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    resident = relationship("Resident", foreign_keys=[resident_id])
    guard = relationship("SecurityGuard", foreign_keys=[guard_id])
