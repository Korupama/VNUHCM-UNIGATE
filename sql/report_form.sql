drop view if exists report_application;

create or replace view report_application as
    select ho_so_du_thi.cccd, ho_so_du_thi.ma_ho_so_du_thi, ho_so_du_thi.dia_diem_du_thi,
           thi_sinh.ho_ten, thi_sinh.ngay_sinh, thi_sinh.gioi_tinh, thi_sinh.dan_toc, truong_thpt.ten_truong_thpt,
           thi_sinh.so_dien_thoai, thi_sinh.email, thi_sinh.dia_chi_lien_lac, truong_thpt.tinh_thanh_pho
    from ho_so_du_thi join thi_sinh on ho_so_du_thi.cccd = thi_sinh.cccd
        join truong_thpt on thi_sinh.ma_truong_thpt = truong_thpt.ma_truong ;

-- refresh materialized view report_application;
select * from report_application;


select * from report_result where cccd='050107072704'

select * from ket_qua_thi

-- select * from v_report_result

-- drop view if exists v_report_result;
-- DROP VIEW v_report_result CASCADE;

CREATE OR REPLACE VIEW report_result AS
SELECT
    ts.cccd,
    hsdt.ma_ho_so_du_thi,
    ts.ho_ten,
    ts.ngay_sinh,
    tt.ten_truong_thpt AS truong_thpt,
    hsdt.dia_diem_du_thi,
    hsdt.dot_thi,
    kqt.diem_thanh_phan_tieng_viet,
    kqt.diem_thanh_phan_tieng_anh,
    kqt.diem_thanh_phan_toan_hoc,
    kqt.diem_thanh_phan_logic_phan_tich_so_lieu,
    kqt.diem_thanh_phan_suy_luan_khoa_hoc,
    kqt.ket_qua_thi AS tong_diem,
    tt.tinh_thanh_pho as tinh
FROM
    thi_sinh ts
JOIN
    ho_so_du_thi hsdt ON ts.cccd = hsdt.cccd
JOIN
    ket_qua_thi kqt ON ts.cccd = kqt.cccd AND hsdt.dot_thi = kqt.dot_thi
LEFT JOIN
    truong_thpt tt ON ts.ma_truong_thpt = tt.ma_truong;

SELECT * FROM report_result WHERE cccd = '050107072704'
-- order by tong_diem desc limit 1;
