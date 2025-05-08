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


create or replace view v_report_ho_so_du_thi as
    select count(*) as so_ho_so_du_thi,
              sum(case when dot_thi = 1 then 1 else 0 end) as so_ho_so_du_thi_dot_1,
                sum(case when dot_thi = 2 then 1 else 0 end) as so_ho_so_du_thi_dot_2
    from ho_so_du_thi

create or replace view v_report_tinh_thanh_pho as
    select truong_thpt.tinh_thanh_pho,count(ma_ho_so_du_thi) as so_luong
    from ho_so_du_thi join thi_sinh on ho_so_du_thi.cccd = thi_sinh.cccd
        join truong_thpt on thi_sinh.ma_truong_thpt = truong_thpt.ma_truong
    group by truong_thpt.tinh_thanh_pho

select * from v_report_tinh_thanh_pho

create or replace view v_report_nguyen_vong as

    select count(ho_so_xet_tuyen.ma_ho_so_xet_tuyen) as so_luong,
            nganh_dao_tao_dai_hoc.ten_truong_khoa as ten_truong
    from ho_so_xet_tuyen join nguyen_vong_xet_tuyen on ho_so_xet_tuyen.ma_ho_so_xet_tuyen = nguyen_vong_xet_tuyen.ma_ho_so_xet_tuyen
        join nganh_dao_tao_dai_hoc on nguyen_vong_xet_tuyen.ma_nganh = nganh_dao_tao_dai_hoc.ma_nganh
    group by nganh_dao_tao_dai_hoc.ten_truong_khoa
select * from v_report_nguyen_vong

create or replace view v_pho_diem_dot_1 as
select
    sum(case when ket_qua_thi.ket_qua_thi > 0 and ket_qua_thi.ket_qua_thi <= 100 then 1 else 0 end) as diem_0_100,
    sum(case when ket_qua_thi.ket_qua_thi > 100 and ket_qua_thi.ket_qua_thi <= 200 then 1 else 0 end) as diem_100_200,
    sum(case when ket_qua_thi.ket_qua_thi > 200 and ket_qua_thi.ket_qua_thi <= 300 then 1 else 0 end) as diem_200_300,
    sum(case when ket_qua_thi.ket_qua_thi > 300 and ket_qua_thi.ket_qua_thi <= 400 then 1 else 0 end) as diem_300_400,
    sum(case when ket_qua_thi.ket_qua_thi > 400 and ket_qua_thi.ket_qua_thi <= 500 then 1 else 0 end) as diem_400_500,
    sum(case when ket_qua_thi.ket_qua_thi > 500 and ket_qua_thi.ket_qua_thi <= 600 then 1 else 0 end) as diem_500_600,
    sum(case when ket_qua_thi.ket_qua_thi > 600 and ket_qua_thi.ket_qua_thi <= 700 then 1 else 0 end) as diem_600_700,
    sum(case when ket_qua_thi.ket_qua_thi > 700 and ket_qua_thi.ket_qua_thi <= 800 then 1 else 0 end) as diem_700_800,
    sum(case when ket_qua_thi.ket_qua_thi > 800 and ket_qua_thi.ket_qua_thi <= 900 then 1 else 0 end) as diem_800_900,
    sum(case when ket_qua_thi.ket_qua_thi > 900 and ket_qua_thi.ket_qua_thi <= 1000 then 1 else 0 end) as diem_900_1000,
    sum(case when ket_qua_thi.ket_qua_thi > 1000 and ket_qua_thi.ket_qua_thi <= 1100 then 1 else 0 end) as diem_1000_1100,
    sum(case when ket_qua_thi.ket_qua_thi > 1100 and ket_qua_thi.ket_qua_thi <= 1200 then 1 else 0 end) as diem_1100_1200
from ket_qua_thi
where dot_thi = 1
select * from v_pho_diem_dot_1
create or replace view v_pho_diem_dot_2 as
select
    sum(case when ket_qua_thi.ket_qua_thi > 0 and ket_qua_thi.ket_qua_thi <= 100 then 1 else 0 end) as diem_0_100,
    sum(case when ket_qua_thi.ket_qua_thi > 100 and ket_qua_thi.ket_qua_thi <= 200 then 1 else 0 end) as diem_100_200,
    sum(case when ket_qua_thi.ket_qua_thi > 200 and ket_qua_thi.ket_qua_thi <= 300 then 1 else 0 end) as diem_200_300,
    sum(case when ket_qua_thi.ket_qua_thi > 300 and ket_qua_thi.ket_qua_thi <= 400 then 1 else 0 end) as diem_300_400,
    sum(case when ket_qua_thi.ket_qua_thi > 400 and ket_qua_thi.ket_qua_thi <= 500 then 1 else 0 end) as diem_400_500,
    sum(case when ket_qua_thi.ket_qua_thi > 500 and ket_qua_thi.ket_qua_thi <= 600 then 1 else 0 end) as diem_500_600,
    sum(case when ket_qua_thi.ket_qua_thi > 600 and ket_qua_thi.ket_qua_thi <= 700 then 1 else 0 end) as diem_600_700,
    sum(case when ket_qua_thi.ket_qua_thi > 700 and ket_qua_thi.ket_qua_thi <= 800 then 1 else 0 end) as diem_700_800,
    sum(case when ket_qua_thi.ket_qua_thi > 800 and ket_qua_thi.ket_qua_thi <= 900 then 1 else 0 end) as diem_800_900,
    sum(case when ket_qua_thi.ket_qua_thi > 900 and ket_qua_thi.ket_qua_thi <= 1000 then 1 else 0 end) as diem_900_1000,
    sum(case when ket_qua_thi.ket_qua_thi > 1000 and ket_qua_thi.ket_qua_thi <= 1100 then 1 else 0 end) as diem_1000_1100,
    sum(case when ket_qua_thi.ket_qua_thi > 1100 and ket_qua_thi.ket_qua_thi <= 1200 then 1 else 0 end) as diem_1100_1200
from ket_qua_thi
where dot_thi = 2

select * from v_pho_diem_dot_2