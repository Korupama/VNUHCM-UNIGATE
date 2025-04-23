from pydantic import BaseModel, Field
from typing import Optional

class AdmissionPreferenceBase(BaseModel):
    thu_tu_nguyen_vong: int = Field(..., ge=1, description="Priority order")
    ten_nganh: str = Field(..., description="Major name (input from frontend)")
    ten_truong: str = Field(..., description="University name (input from frontend)")

class AdmissionPreferenceCreate(AdmissionPreferenceBase):
    cccd: str = Field(..., description="Citizen ID")

class AdmissionPreferenceResponse(AdmissionPreferenceBase):
    ma_ho_so_xet_tuyen: str = Field(..., description="Application ID")
    diem_xet_tuyen: float = Field(..., description="Admission score (read-only)")
