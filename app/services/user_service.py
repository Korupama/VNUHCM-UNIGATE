from app.models.user import ThiSinh, TaiKhoanThiSinh
from psycopg2.extensions import connection

def register_user(db_connection: connection, thi_sinh: ThiSinh, tai_khoan: TaiKhoanThiSinh):
    with db_connection.cursor() as cursor:
        # Insert into thi_sinh table
        cursor.execute(
            """
            INSERT INTO thi_sinh (cccd, ho_ten, email, so_dien_thoai)
            VALUES (%s, %s, %s, %s)
            """,
            (thi_sinh.cccd, thi_sinh.ho_ten, thi_sinh.email, thi_sinh.so_dien_thoai),
        )
        # Insert into tai_khoan_thi_sinh table
        cursor.execute(
            """
            INSERT INTO tai_khoan_thi_sinh (cccd, mat_khau)
            VALUES (%s, %s)
            """,
            (tai_khoan.cccd, tai_khoan.mat_khau),
        )
    db_connection.commit()
