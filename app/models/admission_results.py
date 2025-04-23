from pydantic import BaseModel, Field
from typing import List, Optional

class AdmissionResultItem(BaseModel):
    thu_tu_nguyen_vong: int = Field(..., description="Priority order")
    ma_ho_so_xet_tuyen: str = Field(..., description="Application ID")
    truong: str = Field(..., description="University name")
    nganh: str = Field(..., description="Major name")
    ma_nganh: str = Field(..., description="Major code")
    diem_chuan: int = Field(..., description="Admission score threshold")
    ket_qua: str = Field(..., description="Admission result (Trúng tuyển/Không trúng tuyển)")
    ghi_chu: Optional[str] = Field(None, description="Additional notes")

class AdmissionResultResponse(BaseModel):
    results: List[AdmissionResultItem] = Field(..., description="List of admission results")
