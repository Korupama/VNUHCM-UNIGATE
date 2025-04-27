from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class ThiSinh(BaseModel):
    cccd: str  # CCCD is a 12-character string (char(12) in SQL)
    ho_ten: str  # varchar(50) in SQL
    gioi_tinh: Optional[str]  # varchar(10) in SQL
    ngay_sinh: Optional[date]
    dan_toc: Optional[str]  # varchar(20) in SQL
    dia_chi_thuong_tru: Optional[str]  # varchar(200) in SQL
    dia_chi_lien_lac: Optional[str]  # varchar(200) in SQL
    truong_thpt_ma_tinh: Optional[int]
    ma_truong_thpt: Optional[int]
    email: Optional[EmailStr]  # varchar(50) in SQL
    so_dien_thoai: Optional[str]  # char(10) in SQL
    khu_vuc_uu_tien: Optional[str]  # char(3) in SQL
    doi_tuong_uu_tien: Optional[int]  # int in SQL

class TaiKhoanThiSinh(BaseModel):
    cccd: str  # CCCD is a 12-character string (char(12) in SQL)
    mat_khau: str  # Password should be hashed, varchar(100) in SQL
