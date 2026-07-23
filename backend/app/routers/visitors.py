from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models.user import User, UserRole
from app.models.resident import Resident
from app.models.visitor import Visitor, VisitorStatus
from app.schemas.visitor import VisitorCreate, VisitorResponse, VisitorCheckIn, VisitorLogResponse
from app.services.visitor_service import VisitorService
from app.utils.auth import get_current_user, require_role

router = APIRouter(prefix="/api/visitors", tags=["Visitors"])


@router.post("/", response_model=VisitorResponse)
async def create_visitor(
    visitor_data: VisitorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.RESIDENT, UserRole.ADMIN))
):
    """Create a new visitor pass (Resident only)."""
    # Get resident
    resident = db.query(Resident).filter(Resident.user_id == current_user.id).first()
    if not resident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resident profile not found"
        )
    
    service = VisitorService(db)
    visitor = service.create_visitor(resident.id, visitor_data)
    return visitor


@router.get("/", response_model=List[VisitorResponse])
async def get_visitors(
    status: Optional[VisitorStatus] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get visitors based on user role."""
    service = VisitorService(db)
    
    if current_user.role == UserRole.RESIDENT:
        resident = db.query(Resident).filter(Resident.user_id == current_user.id).first()
        if not resident:
            return []
        return service.get_visitor_history(resident.id, start_date, end_date)
    
    # Guards and admins can see all visitors
    return service.get_visitor_history(None, start_date, end_date)


@router.get("/active", response_model=List[VisitorResponse])
async def get_active_visitors(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SECURITY_GUARD, UserRole.ADMIN))
):
    """Get all currently checked-in visitors (Guards only)."""
    service = VisitorService(db)
    return service.get_active_visitors()


@router.post("/check-in", response_model=VisitorResponse)
async def check_in_visitor(
    check_in_data: VisitorCheckIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SECURITY_GUARD, UserRole.ADMIN))
):
    """Check in a visitor (Guards only)."""
    from app.models.security_guard import SecurityGuard
    
    guard = db.query(SecurityGuard).filter(SecurityGuard.user_id == current_user.id).first()
    guard_id = guard.id if guard else None
    
    service = VisitorService(db)
    visitor = service.check_in_visitor(guard_id, check_in_data)
    
    if not visitor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid QR code or OTP"
        )
    
    return visitor


@router.post("/{visitor_id}/check-out", response_model=VisitorResponse)
async def check_out_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SECURITY_GUARD, UserRole.ADMIN))
):
    """Check out a visitor (Guards only)."""
    from app.models.security_guard import SecurityGuard
    
    guard = db.query(SecurityGuard).filter(SecurityGuard.user_id == current_user.id).first()
    guard_id = guard.id if guard else None
    
    service = VisitorService(db)
    visitor = service.check_out_visitor(visitor_id, guard_id)
    
    if not visitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visitor not found or not checked in"
        )
    
    return visitor


@router.post("/{visitor_id}/resend-otp")
async def resend_otp(
    visitor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.RESIDENT, UserRole.ADMIN))
):
    """Resend OTP to visitor."""
    service = VisitorService(db)
    otp = service.generate_and_send_otp(visitor_id)
    
    if not otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not generate OTP"
        )
    
    return {"message": "OTP sent successfully"}


@router.get("/{visitor_id}", response_model=VisitorResponse)
async def get_visitor(
    visitor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get visitor details."""
    visitor = db.query(Visitor).filter(Visitor.id == visitor_id).first()
    
    if not visitor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visitor not found"
        )
    
    return visitor
