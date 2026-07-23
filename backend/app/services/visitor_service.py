from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from app.models.visitor import Visitor, VisitorLog, VisitorStatus
from app.models.resident import Resident
from app.schemas.visitor import VisitorCreate, VisitorCheckIn
from app.utils.qr_generator import generate_qr_code
from app.utils.otp import generate_otp, get_otp_expiry, verify_otp, send_otp_sms
from app.utils.notifications import send_visitor_notification


class VisitorService:
    def __init__(self, db: Session):
        self.db = db

    def create_visitor(self, resident_id: int, visitor_data: VisitorCreate) -> Visitor:
        """Create a new visitor pass."""
        # Generate QR code
        qr_code, qr_token = generate_qr_code(f"visitor:{resident_id}")
        
        visitor = Visitor(
            resident_id=resident_id,
            name=visitor_data.name,
            phone=visitor_data.phone,
            email=visitor_data.email,
            purpose=visitor_data.purpose,
            expected_arrival=visitor_data.expected_arrival,
            expected_departure=visitor_data.expected_departure,
            qr_code=qr_code,
            qr_token=qr_token,
            status=VisitorStatus.APPROVED,
            notes=visitor_data.notes
        )
        
        self.db.add(visitor)
        self.db.commit()
        self.db.refresh(visitor)
        
        # Send OTP if phone provided
       ### if visitor.phone:
            #self.generate_and_send_otp(visitor.id)
        
        return visitor

    def generate_and_send_otp(self, visitor_id: int) -> Optional[str]:
        """Generate and send OTP for visitor verification."""
        visitor = self.db.query(Visitor).filter(Visitor.id == visitor_id).first()
        if not visitor or not visitor.phone:
            return None
        
        otp = generate_otp()
        visitor.otp = otp
        visitor.otp_expires_at = get_otp_expiry()
        self.db.commit()
        
        send_otp_sms(visitor.phone, otp)
        return otp

    def verify_visitor_otp(self, visitor_id: int, otp: str) -> bool:
        """Verify visitor OTP."""
        visitor = self.db.query(Visitor).filter(Visitor.id == visitor_id).first()
        if not visitor or not visitor.otp or not visitor.otp_expires_at:
            return False
        
        return verify_otp(visitor.otp, otp, visitor.otp_expires_at)

    def check_in_visitor(
        self,
        guard_id: int,
        check_in_data: VisitorCheckIn
    ) -> Optional[Visitor]:
        """Check in a visitor using QR token or OTP."""
        visitor = None
        
        if check_in_data.qr_token:
            visitor = self.db.query(Visitor).filter(
                Visitor.qr_token == check_in_data.qr_token,
                Visitor.status == VisitorStatus.APPROVED
            ).first()
        
        if not visitor:
            return None
        
        # Verify OTP if provided
        if check_in_data.otp:
            if not self.verify_visitor_otp(visitor.id, check_in_data.otp):
                return None
        
        # Update status
        visitor.status = VisitorStatus.CHECKED_IN
        
        # Create log entry
        log = VisitorLog(
            visitor_id=visitor.id,
            guard_id=guard_id,
            action="check_in",
            notes=check_in_data.notes,
            photo_at_entry=check_in_data.photo_at_entry
        )
        self.db.add(log)
        self.db.commit()
        
        # Send notification
        resident = self.db.query(Resident).filter(Resident.id == visitor.resident_id).first()
        if resident and resident.user:
            send_visitor_notification(resident.user.email, visitor.name, "entered")
        
        return visitor

    def check_out_visitor(self, visitor_id: int, guard_id: int) -> Optional[Visitor]:
        """Check out a visitor."""
        visitor = self.db.query(Visitor).filter(
            Visitor.id == visitor_id,
            Visitor.status == VisitorStatus.CHECKED_IN
        ).first()
        
        if not visitor:
            return None
        
        visitor.status = VisitorStatus.CHECKED_OUT
        
        log = VisitorLog(
            visitor_id=visitor.id,
            guard_id=guard_id,
            action="check_out"
        )
        self.db.add(log)
        self.db.commit()
        
        return visitor

    def get_visitor_history(
        self,
        resident_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Visitor]:
        """Get visitor history with optional filters."""
        query = self.db.query(Visitor)
        
        if resident_id:
            query = query.filter(Visitor.resident_id == resident_id)
        if start_date:
            query = query.filter(Visitor.created_at >= start_date)
        if end_date:
            query = query.filter(Visitor.created_at <= end_date)
        
        return query.order_by(Visitor.created_at.desc()).all()

    def get_active_visitors(self) -> List[Visitor]:
        """Get all currently checked-in visitors."""
        return self.db.query(Visitor).filter(
            Visitor.status == VisitorStatus.CHECKED_IN
        ).all()
