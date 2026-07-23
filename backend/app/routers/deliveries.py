from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User, UserRole
from app.models.resident import Resident
from app.models.delivery import Delivery, DeliveryStatus
from app.models.security_guard import SecurityGuard
from app.schemas.delivery import DeliveryCreate, DeliveryResponse, DeliveryUpdate
from app.utils.auth import get_current_user, require_role
from app.utils.notifications import send_delivery_notification

router = APIRouter(prefix="/api/deliveries", tags=["Deliveries"])


@router.post("/", response_model=DeliveryResponse)
async def create_delivery(
    delivery_data: DeliveryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SECURITY_GUARD, UserRole.ADMIN))
):
    """Register a new delivery (Guards only)."""
    # Get guard info
    guard = db.query(SecurityGuard).filter(SecurityGuard.user_id == current_user.id).first()
    
    # Verify resident exists
    resident = db.query(Resident).filter(Resident.id == delivery_data.resident_id).first()
    if not resident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resident not found"
        )
    
    delivery = Delivery(
        resident_id=delivery_data.resident_id,
        guard_id=guard.id if guard else None,
        courier_name=delivery_data.courier_name,
        courier_company=delivery_data.courier_company,
        tracking_number=delivery_data.tracking_number,
        package_description=delivery_data.package_description,
        status=DeliveryStatus.RECEIVED_AT_GATE,
        notes=delivery_data.notes
    )
    
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    
    # Send notification
    if resident.user:
        await send_delivery_notification(
            resident.user.email,
            delivery.courier_company or "Unknown",
            delivery.tracking_number or "N/A"
        )
    
    return delivery


@router.get("/", response_model=List[DeliveryResponse])
async def get_deliveries(
    status: Optional[DeliveryStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get deliveries based on user role."""
    query = db.query(Delivery)
    
    if current_user.role == UserRole.RESIDENT:
        resident = db.query(Resident).filter(Resident.user_id == current_user.id).first()
        if not resident:
            return []
        query = query.filter(Delivery.resident_id == resident.id)
    
    if status:
        query = query.filter(Delivery.status == status)
    
    return query.order_by(Delivery.created_at.desc()).all()


@router.patch("/{delivery_id}", response_model=DeliveryResponse)
async def update_delivery(
    delivery_id: int,
    update_data: DeliveryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update delivery status."""
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery not found"
        )
    
    if update_data.status:
        delivery.status = update_data.status
        if update_data.status == DeliveryStatus.DELIVERED:
            from datetime import datetime
            delivery.delivered_at = datetime.utcnow()
    
    if update_data.notes:
        delivery.notes = update_data.notes
    
    db.commit()
    db.refresh(delivery)
    
    return delivery


@router.get("/pending", response_model=List[DeliveryResponse])
async def get_pending_deliveries(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.SECURITY_GUARD, UserRole.ADMIN))
):
    """Get all pending deliveries at gate."""
    return db.query(Delivery).filter(
        Delivery.status.in_([DeliveryStatus.RECEIVED_AT_GATE, DeliveryStatus.IN_TRANSIT])
    ).all()
