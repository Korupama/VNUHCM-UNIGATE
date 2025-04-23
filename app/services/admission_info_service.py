import psycopg2
from psycopg2.extras import RealDictCursor

def get_admission_info(cccd: str):
    """
    Fetch admission information including application ID, CCCD, exam scores, priority area,
    priority group, admission score, and application fee.
    """
    query = """
        SELECT 
            ma_ho_so_xet_tuyen,
            cccd,
            diem_thi,
            khu_vuc_uu_tien,
            doi_tuong_uu_tien,
            diem_xet_tuyen,
            le_phi_xet_tuyen
        FROM ho_so_xet_tuyen
        WHERE cccd = %s
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (cccd,))
        result = cur.fetchone()
    if result:
        return result
    else:
        return {"message": "No admission information found for the provided CCCD."}
