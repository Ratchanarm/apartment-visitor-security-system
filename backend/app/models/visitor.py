from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Text
from app.database import Base
import enum


class VisitorStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(255))
    purpose = Column(String(200))
    expected_arrival = Column(DateTime(timezone=True))
    expected_departure = Column(DateTime(timezone=True))
    qr_code = Column(Text)
    qr_token = Column(String(100), unique=True, index=True)
    otp = Column(String(10))
    otp_expires_at = Column(DateTime(timezone=True))
    status = Column(SQLEnum(VisitorStatus), default=VisitorStatus.PENDING)
    photo_url = Column(String(500))
    id_proof_url = Column(String(500))
    face_encoding = Column(Text)  # Stored as JSON for face recognition
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    resident = relationship("Resident", back_populates="visitors")
    logs = relationship("VisitorLog", back_populates="visitor")


class VisitorLog(Base):
    __tablename__ = "visitor_logs"

    id = Column(Integer, primary_key=True, index=True)
    visitor_id = Column(Integer, ForeignKey("visitors.id"), nullable=False)
    guard_id = Column(Integer, ForeignKey("security_guards.id"))
    action = Column(String(50), nullable=False)  # check_in, check_out, denied
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    photo_at_entry = Column(String(500))

    visitor = relationship("Visitor", back_populates="logs")
    guard = relationship("SecurityGuard")
