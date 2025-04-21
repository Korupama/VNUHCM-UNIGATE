from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from app.models.exam_registration import (
    ExamRegistrationCreate, 
    ExamRegistrationResponse,
    ExamRegistrationUpdate
)
from app.services.exam_registration_service import ExamRegistrationService

router = APIRouter(
    prefix="/api/exam-registration",
    tags=["exam-registration"],
    responses={404: {"description": "Not found"}},
)

# Simple authentication scheme - in a real app this would be more robust
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Simple function that returns the user's CCCD from token.
    In a real app, this would validate the token and extract user info.
    """
    # For demo purposes, we're assuming the token is the CCCD itself
    return token

def get_registration_service(conn=Depends(lambda: router.db_connection)):
    """Dependency to get the exam registration service with DB connection"""
    return ExamRegistrationService(conn)


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED, 
    response_model=ExamRegistrationResponse,
    summary="Register for an exam session",
    description="Create a new exam registration for a specific exam session (dot_thi)"
)
async def register_for_exam(
    registration_data: ExamRegistrationCreate,
    service: ExamRegistrationService = Depends(get_registration_service),
    cccd: str = Depends(get_current_user)
):
    # Create the registration
    result = service.create_registration(
        cccd=cccd,
        dia_diem_du_thi=registration_data.dia_diem_du_thi,
        dot_thi=registration_data.dot_thi
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Registration already exists for CCCD {cccd} and exam session {registration_data.dot_thi}"
        )
    
    return result


@router.get(
    "/", 
    response_model=List[ExamRegistrationResponse],
    summary="Get user's exam registrations",
    description="Retrieve all exam registrations for the authenticated user"
)
async def get_user_registrations(
    service: ExamRegistrationService = Depends(get_registration_service),
    cccd: str = Depends(get_current_user)
):
    registrations = service.get_registrations_by_cccd(cccd)
    if not registrations:
        return []
    return registrations


@router.get(
    "/{dot_thi}", 
    response_model=ExamRegistrationResponse,
    summary="Get specific exam registration",
    description="Retrieve exam registration details for a specific exam session"
)
async def get_registration_by_session(
    dot_thi: int = Path(..., ge=1, le=2, description="Exam session (1 or 2)"),
    service: ExamRegistrationService = Depends(get_registration_service),
    cccd: str = Depends(get_current_user)
):
    registration = service.get_registration(cccd, dot_thi)
    if not registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No registration found for CCCD {cccd} and exam session {dot_thi}"
        )
    return registration


@router.patch(
    "/{dot_thi}", 
    response_model=ExamRegistrationResponse,
    summary="Update exam location",
    description="Update the exam location for an existing registration"
)
async def update_exam_location(
    update_data: ExamRegistrationUpdate,
    dot_thi: int = Path(..., ge=1, le=2, description="Exam session (1 or 2)"),
    service: ExamRegistrationService = Depends(get_registration_service),
    cccd: str = Depends(get_current_user)
):
    # Verify that the registration exists first
    existing_registration = service.get_registration(cccd, dot_thi)
    if not existing_registration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No registration found for CCCD {cccd} and exam session {dot_thi}"
        )
    
    # Only allow updating the exam location
    if update_data.dia_diem_du_thi:
        result = service.update_registration_location(
            cccd=cccd,
            dot_thi=dot_thi,
            dia_diem_du_thi=update_data.dia_diem_du_thi
        )
        return result
    
    # If no location update provided, return existing registration
    return existing_registration
