from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.user import User, UserRole
from app.models.resident import Resident
from app.models.security_guard import SecurityGuard
from app.models.emergency_alert import EmergencyAlert
from app.schemas.emergency import EmergencyAlertCreate, EmergencyAlertResponse
from app.utils.auth import get_current_user, require_role
from app.utils.notifications import send_emergency_notification

router = APIRouter(prefix="/api/emergency", tags=["Emergency"])


@router.post("/", response_model=EmergencyAlertResponse)
async def create_emergency_alert(
    alert_data: EmergencyAlertCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create an emergency alert."""
    resident_id = None
    guard_id = None
    
    if current_user.role == UserRole.RESIDENT:
        resident = db.query(Resident).filter(Resident.user_id == current_user.id).first()
        resident_id = resident.id if resident else None
    elif current_user.role == UserRole.SECURITY_GUARD:
        guard = db.query(SecurityGuard).filter(SecurityGuard.user_id == current_user.id).first()
        guard_id = guard.id if guard else None
    
    alert = EmergencyAlert(
        resident_id=resident_id,
        guard_id=guard_id,
        alert_type=alert_data.alert_type,
        priority=alert_data.priority,
        title=alert_data.title,
        description=alert_data.description,
        location=alert_data.location
    )
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    # Notify all guards and admins
    users = db.query(User).filter(
        User.role.in_([UserRole.SECURITY_GUARD, UserRole.ADMIN]),
        User.is_active == True
    ).all()
    
    emails = [u.email for u in users if u.email]
    await send_emergency_notification(
        emails,
        alert.alert_type.value,
        alert.title,
        alert.description or ""
    )
    
    return alert


@router.get("/", response_model=List[EmergencyAlertResponse])
async def get_emergency_alerts(
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get emergency alerts."""
    query = db.query(EmergencyAlert)
    
    if active_only:
        query = query.filter(EmergencyAlert.is_resolved == False)
    
    return query.order_by(EmergencyAlert.created_at.desc()).all()


@router.post("/{alert_id}/resolve", response_model=EmergencyAlertResponse)
async def resolve_emergency(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SECURITY_GUARD, UserRole.ADMIN))
):
    """Resolve an emergency alert."""
    alert = db.query(EmergencyAlert).filter(EmergencyAlert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    alert.is_resolved = True
    alert.resolved_at = datetime.utcnow()
    alert.resolved_by = current_user.id
    
    db.commit()
    db.refresh(alert)
    
    return alert
