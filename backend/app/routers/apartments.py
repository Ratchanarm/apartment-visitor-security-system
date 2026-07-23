from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.models.apartment import Apartment
from app.models.resident import Resident
from app.schemas.apartment import ApartmentCreate, ApartmentResponse
from app.schemas.resident import ResidentCreate, ResidentResponse
from app.utils.auth import get_current_user, require_role

router = APIRouter(prefix="/api/apartments", tags=["Apartments"])


@router.post("/", response_model=ApartmentResponse)
async def create_apartment(
    apartment_data: ApartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Create a new apartment (Admin only)."""
    apartment = Apartment(**apartment_data.model_dump())
    db.add(apartment)
    db.commit()
    db.refresh(apartment)
    return apartment


@router.get("/", response_model=List[ApartmentResponse])
async def get_apartments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all apartments."""
    return db.query(Apartment).all()


@router.get("/{apartment_id}", response_model=ApartmentResponse)
async def get_apartment(
    apartment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get apartment details."""
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not found"
        )
    return apartment


@router.post("/{apartment_id}/residents", response_model=ResidentResponse)
async def add_resident(
    apartment_id: int,
    resident_data: ResidentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Add a resident to an apartment (Admin only)."""
    apartment = db.query(Apartment).filter(Apartment.id == apartment_id).first()
    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not found"
        )
    
    resident = Resident(
        user_id=resident_data.user_id,
        apartment_id=apartment_id,
        is_owner=resident_data.is_owner,
        emergency_contact=resident_data.emergency_contact
    )
    db.add(resident)
    db.commit()
    db.refresh(resident)
    return resident
