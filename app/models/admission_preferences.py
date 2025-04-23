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


class AdmissionPreferenceUpdate(BaseModel):
    ma_nganh: Optional[str] = Field(None, description="Major code")
    thu_tu_nguyen_vong: Optional[int] = Field(None, ge=1, description="Priority order")
    ten_nganh: Optional[str] = Field(None, description="Major name (optional for updates)")
    ten_truong: Optional[str] = Field(None, description="University name (optional for updates)")