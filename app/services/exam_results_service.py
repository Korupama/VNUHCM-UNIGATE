import psycopg2
from psycopg2.extras import RealDictCursor

def get_exam_results_by_session(cccd: str, session: int):
    """
    Fetch exam results for a specific session from the database.
    """
    query = """
        SELECT 
            diem_thanh_phan_tieng_viet,
            diem_thanh_phan_tieng_anh,
            diem_thanh_phan_toan_hoc,
            diem_thanh_phan_logic_phan_tich_so_lieu,
            diem_thanh_phan_suy_luan_khoa_hoc,
            ket_qua_thi
        FROM ket_qua_thi
        WHERE cccd = %s AND dot_thi = %s
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(query, (cccd, session))
        result = cur.fetchone()
    if result:
        return result
    else:
        return {"message": f"No results found for session {session}."}
