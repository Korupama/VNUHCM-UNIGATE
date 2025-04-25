from fastapi import APIRouter, HTTPException, Depends
from app.models.user import ThiSinh
from app.services.user_update_service import update_user_info
from psycopg2.extensions import connection

router = APIRouter()

@router.put("/api/update-user")
def update_user(
    cccd: str,
    updated_data: ThiSinh,
    is_admin: bool = False,  # Simulate admin check
    db_connection: connection = Depends(lambda: router.db_connection),
):
    try:
        # Ensure non-admins cannot update doi_tuong_uu_tien
        if not is_admin and updated_data.doi_tuong_uu_tien is not None:
            raise HTTPException(status_code=403, detail="Only admins can update doi_tuong_uu_tien")

        # Call service to update user info
        update_user_info(db_connection, cccd, updated_data, is_admin)
        return {"message": "User information updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
