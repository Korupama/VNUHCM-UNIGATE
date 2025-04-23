from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.admission_preferences import (
    AdmissionPreferenceCreate,
    AdmissionPreferenceResponse,
    AdmissionPreferenceUpdate
)
from app.services.admission_preferences_service import AdmissionPreferencesService

router = APIRouter(
    prefix="/api/admission-preferences",
    tags=["Admission Preferences"],
    responses={404: {"description": "Not found"}},
)

def get_preferences_service(conn=Depends(lambda: router.db_connection)):
    """Dependency to get the admission preferences service with DB connection"""
    return AdmissionPreferencesService(conn)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=AdmissionPreferenceResponse,
    summary="Add a new admission preference",
    description="Create a new admission preference for a specific application ID"
)
async def add_preference(
    preference_data: AdmissionPreferenceCreate,
    service: AdmissionPreferencesService = Depends(get_preferences_service)
):
    result = service.create_preference(preference_data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Preference already exists for the given application ID and priority order"
        )
    return result

@router.get(
    "/",
    response_model=List[AdmissionPreferenceResponse],
    summary="Get all admission preferences",
    description="Retrieve all admission preferences for a specific application ID"
)
async def get_preferences(
    application_id: str,
    service: AdmissionPreferencesService = Depends(get_preferences_service)
):
    preferences = service.get_preferences_by_application_id(application_id)
    if not preferences:
        return []
    return preferences

@router.patch(
    "/{priority_order}",
    response_model=AdmissionPreferenceResponse,
    summary="Update an admission preference",
    description="Update the details of an existing admission preference"
)
async def update_preference(
    priority_order: int,
    update_data: AdmissionPreferenceUpdate,
    application_id: str,
    service: AdmissionPreferencesService = Depends(get_preferences_service)
):
    existing_preference = service.get_preference(application_id, priority_order)
    if not existing_preference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No preference found for the given application ID and priority order"
        )
    result = service.update_preference(application_id, priority_order, update_data)
    return result

@router.delete(
    "/{priority_order}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an admission preference",
    description="Delete an existing admission preference"
)
async def delete_preference(
    priority_order: int,
    application_id: str,
    service: AdmissionPreferencesService = Depends(get_preferences_service)
):
    existing_preference = service.get_preference(application_id, priority_order)
    if not existing_preference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No preference found for the given application ID and priority order"
        )
    service.delete_preference(application_id, priority_order)
