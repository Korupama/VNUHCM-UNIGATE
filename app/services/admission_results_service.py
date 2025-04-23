import psycopg2
from psycopg2.extras import RealDictCursor

class AdmissionResultsService:
    def __init__(self, conn):
        self.conn = conn

    def get_results_by_application_id(self, application_id: str):
        """
        Fetch admission results for a specific application ID.
        """
        query = """
            SELECT 
                thu_tu_nguyen_vong,
                ma_ho_so_xet_tuyen,
                ten_truong_khoa AS truong,
                ten_nganh AS nganh,
                ma_nganh,
                diem_chuan_nam_truoc AS diem_chuan,
                CASE 
                    WHEN diem_xet_tuyen >= diem_chuan_nam_truoc THEN 'Trúng tuyển'
                    ELSE 'Không trúng tuyển'
                END AS ket_qua,
                CASE 
                    WHEN diem_xet_tuyen >= diem_chuan_nam_truoc THEN NULL
                    ELSE 'Điểm xét tuyển thấp hơn điểm chuẩn'
                END AS ghi_chu
            FROM nguyen_vong_xet_tuyen
            JOIN nganh_dao_tao_dai_hoc ON nguyen_vong_xet_tuyen.ma_nganh = nganh_dao_tao_dai_hoc.ma_nganh
            WHERE ma_ho_so_xet_tuyen = %s
            ORDER BY thu_tu_nguyen_vong
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (application_id,))
            return cur.fetchall()
