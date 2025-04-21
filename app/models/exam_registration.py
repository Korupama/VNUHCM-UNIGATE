from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum


class ExamSessionEnum(int, Enum):
    SESSION_1 = 1
    SESSION_2 = 2


class ExamRegistrationBase(BaseModel):
    dia_diem_du_thi: str = Field(..., min_length=5, max_length=100, description="Location where the candidate will take the exam")
    dot_thi: ExamSessionEnum = Field(..., description="Exam session (1 or 2)")


class ExamRegistrationCreate(ExamRegistrationBase):
    pass


class ExamRegistrationResponse(ExamRegistrationBase):
    ma_ho_so_du_thi: str = Field(..., description="Registration ID (auto-generated)")
    cccd: str = Field(..., description="Citizen ID card number")
    tinh_trang_thanh_toan: str = Field(default="chua_thanh_toan", description="Payment status")
    le_phi_thi: float = Field(default=300000.0, description="Exam fee")
    thoi_gian_thanh_toan_le_phi_thi: Optional[str] = Field(None, description="Payment timestamp")


class ExamRegistrationUpdate(BaseModel):
    dia_diem_du_thi: Optional[str] = Field(None, min_length=5, max_length=100, description="Location where the candidate will take the exam")
