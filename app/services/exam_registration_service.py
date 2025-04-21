from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime


class ExamRegistrationService:
    def __init__(self, db_connection):
        self.conn = db_connection

    def generate_registration_id(self, cccd: str, dot_thi: int) -> str:
        """Generate registration ID based on CCCD and exam session"""
        if dot_thi == 1:
            return f"HS{cccd}"
        else:  # dot_thi == 2
            return f"H2{cccd}"

    def create_registration(self, cccd: str, dia_diem_du_thi: str, dot_thi: int) -> dict:
        """Create a new exam registration record"""
        ma_ho_so_du_thi = self.generate_registration_id(cccd, dot_thi)
        le_phi_thi = 300000.0

        # Check if registration already exists
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM ho_so_du_thi WHERE cccd = %s AND dot_thi = %s",
                (cccd, dot_thi)
            )
            existing_registration = cursor.fetchone()
            if existing_registration:
                return None  # Registration already exists

            # Create new registration
            cursor.execute(
                """
                INSERT INTO ho_so_du_thi 
                (ma_ho_so_du_thi, cccd, dia_diem_du_thi, tinh_trang_thanh_toan, le_phi_thi, dot_thi) 
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (ma_ho_so_du_thi, cccd, dia_diem_du_thi, "chua_thanh_toan", le_phi_thi, dot_thi)
            )
            self.conn.commit()
            return cursor.fetchone()

    def get_registration(self, cccd: str, dot_thi: int) -> dict:
        """Get exam registration details by CCCD and exam session"""
        ma_ho_so_du_thi = self.generate_registration_id(cccd, dot_thi)
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM ho_so_du_thi WHERE ma_ho_so_du_thi = %s",
                (ma_ho_so_du_thi,)
            )
            return cursor.fetchone()
    
    def get_registrations_by_cccd(self, cccd: str) -> list:
        """Get all exam registrations for a candidate by CCCD"""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM ho_so_du_thi WHERE cccd = %s",
                (cccd,)
            )
            return cursor.fetchall()

    def update_registration_location(self, cccd: str, dot_thi: int, dia_diem_du_thi: str) -> dict:
        """Update the exam location for an existing registration"""
        ma_ho_so_du_thi = self.generate_registration_id(cccd, dot_thi)
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE ho_so_du_thi 
                SET dia_diem_du_thi = %s
                WHERE ma_ho_so_du_thi = %s
                RETURNING *
                """,
                (dia_diem_du_thi, ma_ho_so_du_thi)
            )
            self.conn.commit()
            return cursor.fetchone()
