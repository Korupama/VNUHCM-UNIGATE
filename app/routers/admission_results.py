from fastapi import APIRouter, HTTPException, Depends
from app.services.admission_results_service import AdmissionResultsService
from app.models.admission_results import AdmissionResultResponse

router = APIRouter(
    prefix="/api/admission-results",
    tags=["Admission Results"],
    responses={404: {"description": "Not found"}},
)

def get_results_service(conn=Depends(lambda: router.db_connection)):
    """Dependency to get the admission results service with DB connection"""
    return AdmissionResultsService(conn)

@router.get(
    "/",
    response_model=AdmissionResultResponse,
    summary="Get admission results",
    description="Retrieve admission results for a specific application ID"
)
async def get_admission_results(
    application_id: str,
    service: AdmissionResultsService = Depends(get_results_service)
):
    results = service.get_results_by_application_id(application_id)
    if not results:
        raise HTTPException(
            status_code=404,
            detail="No admission results available for the provided application ID."
        )
    return results
