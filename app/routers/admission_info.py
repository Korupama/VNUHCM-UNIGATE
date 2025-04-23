from fastapi import APIRouter
from app.services.admission_info_service import get_admission_info

router = APIRouter(
    prefix="/api/admission-info",
    tags=["Admission Information"]
)

@router.get("/")
def fetch_admission_info(cccd: str):
    """
    Fetch admission information including application ID, CCCD, exam scores, priority area,
    priority group, admission score, and application fee.
    """
    return get_admission_info(cccd)
