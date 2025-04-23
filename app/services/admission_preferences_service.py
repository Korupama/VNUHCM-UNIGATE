import psycopg2
from psycopg2.extras import RealDictCursor
from app.models.admission_preferences import AdmissionPreferenceCreate, AdmissionPreferenceUpdate

class AdmissionPreferencesService:
    def __init__(self, conn):
        self.conn = conn

    def create_preference(self, preference_data: AdmissionPreferenceCreate):
        # Validate that the major and university exist in nganh_dao_tao_dai_hoc
        major_query = """
            SELECT ma_nganh, ten_nganh FROM nganh_dao_tao_dai_hoc 
            WHERE ten_nganh = %s AND ten_truong_khoa = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(major_query, (preference_data.ten_nganh, preference_data.ten_truong))
            major = cur.fetchone()
            if not major:
                raise ValueError(f"Major '{preference_data.ten_nganh}' at university '{preference_data.ten_truong}' does not exist.")

        # Fetch ma_ho_so_xet_tuyen and diem_xet_tuyen from ho_so_xet_tuyen
        application_query = """
            SELECT ma_ho_so_xet_tuyen, diem_xet_tuyen FROM ho_so_xet_tuyen WHERE cccd = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(application_query, (preference_data.cccd,))
            application = cur.fetchone()
            if not application:
                raise ValueError(f"No application found for CCCD {preference_data.cccd}.")

        # Check if the priority order already exists for the application
        priority_check_query = """
            SELECT * FROM nguyen_vong_xet_tuyen 
            WHERE ma_ho_so_xet_tuyen = %s AND thu_tu_nguyen_vong = %s
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(priority_check_query, (application["ma_ho_so_xet_tuyen"], preference_data.thu_tu_nguyen_vong))
            existing_priority = cur.fetchone()
            if existing_priority:
                raise ValueError(f"Priority order {preference_data.thu_tu_nguyen_vong} already exists for application ID {application['ma_ho_so_xet_tuyen']}.")

        # Check if the major code or major name already exists for the candidate
        major_check_query = """
            SELECT * FROM nguyen_vong_xet_tuyen 
            WHERE cccd = %s AND (ma_nganh = %s OR EXISTS (
                SELECT 1 FROM nganh_dao_tao_dai_hoc 
                WHERE nganh_dao_tao_dai_hoc.ma_nganh = nguyen_vong_xet_tuyen.ma_nganh 
                AND nganh_dao_tao_dai_hoc.ten_nganh = %s
            ))
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(major_check_query, (preference_data.cccd, major["ma_nganh"], preference_data.ten_nganh))
            existing_major = cur.fetchone()
            if existing_major:
                raise ValueError(f"Major '{preference_data.ten_nganh}' or code '{major['ma_nganh']}' already exists for CCCD {preference_data.cccd}.")

        # Insert into nguyen_vong_xet_tuyen
        insert_query = """
            INSERT INTO nguyen_vong_xet_tuyen (ma_ho_so_xet_tuyen, cccd, ma_nganh, thu_tu_nguyen_vong, diem_xet_tuyen)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(insert_query, (
                application["ma_ho_so_xet_tuyen"],
                preference_data.cccd,
                major["ma_nganh"],
                preference_data.thu_tu_nguyen_vong,
                application["diem_xet_tuyen"]
            ))
            self.conn.commit()
            return cur.fetchone()
