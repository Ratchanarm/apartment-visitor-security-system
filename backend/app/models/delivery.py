from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class DeliveryStatus(str, enum.Enum):
    PENDING = "pending"
    RECEIVED_AT_GATE = "received_at_gate"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    RETURNED = "returned"


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)
    guard_id = Column(Integer, ForeignKey("security_guards.id"))
    courier_name = Column(String(100))
    courier_company = Column(String(100))
    tracking_number = Column(String(100))
    package_description = Column(String(500))
    photo_url = Column(String(500))
    status = Column(SQLEnum(DeliveryStatus), default=DeliveryStatus.PENDING)
    received_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    signature_url = Column(String(500))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    resident = relationship("Resident")
    guard = relationship("SecurityGuard")
