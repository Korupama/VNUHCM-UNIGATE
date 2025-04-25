from fastapi import APIRouter, HTTPException, Depends
from app.models.user import ThiSinh, TaiKhoanThiSinh
from app.services.user_service import register_user
from psycopg2.extensions import connection

router = APIRouter()

@router.post("/api/register")
def register_user_api(
    thi_sinh: ThiSinh,
    tai_khoan: TaiKhoanThiSinh,
    db_connection: connection = Depends(lambda: router.db_connection),
):
    try:
        register_user(db_connection, thi_sinh, tai_khoan)
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
