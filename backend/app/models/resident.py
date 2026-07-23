from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Resident(Base):
    __tablename__ = "residents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    apartment_id = Column(Integer, ForeignKey("apartments.id"), nullable=False)
    is_owner = Column(Boolean, default=False)
    move_in_date = Column(DateTime(timezone=True))
    emergency_contact = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    apartment = relationship("Apartment", back_populates="residents")
    visitors = relationship("Visitor", back_populates="resident")
