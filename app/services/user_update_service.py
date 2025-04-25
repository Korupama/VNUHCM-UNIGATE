from app.models.user import ThiSinh
from psycopg2.extensions import connection

def update_user_info(db_connection: connection, cccd: str, updated_data: ThiSinh, is_admin: bool):
    with db_connection.cursor() as cursor:
        # Query khu_vuc_uu_tien based on ma_truong_thpt and truong_thpt_ma_tinh
        cursor.execute(
            """
            SELECT khu_vuc_xet_tuyen
            FROM truong_thpt
            WHERE ma_truong = %s AND ma_tinh_thanh_pho = %s
            """,
            (updated_data.ma_truong_thpt, updated_data.truong_thpt_ma_tinh),
        )
        khu_vuc_uu_tien = cursor.fetchone()
        if not khu_vuc_uu_tien:
            raise ValueError("Invalid ma_truong_thpt or truong_thpt_ma_tinh")

        # Update thi_sinh table
        cursor.execute(
            """
            UPDATE thi_sinh
            SET ho_ten = %s,
                gioi_tinh = %s,
                ngay_sinh = %s,
                dan_toc = %s,
                dia_chi_thuong_tru = %s,
                dia_chi_lien_lac = %s,
                truong_thpt_ma_tinh = %s,
                ma_truong_thpt = %s,
                email = %s,
                so_dien_thoai = %s,
                khu_vuc_uu_tien = %s,
                doi_tuong_uu_tien = %s
            WHERE cccd = %s
            """,
            (
                updated_data.ho_ten,
                updated_data.gioi_tinh,
                updated_data.ngay_sinh,
                updated_data.dan_toc,
                updated_data.dia_chi_thuong_tru,
                updated_data.dia_chi_lien_lac,
                updated_data.truong_thpt_ma_tinh,
                updated_data.ma_truong_thpt,
                updated_data.email,
                updated_data.so_dien_thoai,
                khu_vuc_uu_tien[0],  # Extract value from query result
                updated_data.doi_tuong_uu_tien if is_admin else None,
                cccd,
            ),
        )
    db_connection.commit()
