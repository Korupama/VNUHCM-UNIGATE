from fastapi import APIRouter, Depends
from app.services.exam_results_service import get_exam_results_by_session

router = APIRouter(
    prefix="/api/exam-results",
    tags=["Exam Results"]
)

@router.get("/session-1")
def get_session_1_results(cccd: str):
    """
    Fetch exam results for session 1.
    """
    return get_exam_results_by_session(cccd, 1)

@router.get("/session-2")
def get_session_2_results(cccd: str):
    """
    Fetch exam results for session 2.
    """
    return get_exam_results_by_session(cccd, 2)
