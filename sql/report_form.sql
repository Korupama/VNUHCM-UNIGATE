drop view if exists report_application;

create or replace view report_application as
    select ho_so_du_thi.cccd, ho_so_du_thi.ma_ho_so_du_thi, ho_so_du_thi.dia_diem_du_thi,
           thi_sinh.ho_ten, thi_sinh.ngay_sinh, thi_sinh.gioi_tinh, thi_sinh.dan_toc, truong_thpt.ten_truong_thpt,
           thi_sinh.so_dien_thoai, thi_sinh.email, thi_sinh.dia_chi_lien_lac, truong_thpt.tinh_thanh_pho
    from ho_so_du_thi join thi_sinh on ho_so_du_thi.cccd = thi_sinh.cccd
        join truong_thpt on thi_sinh.ma_truong_thpt = truong_thpt.ma_truong ;

-- refresh materialized view report_application;
select * from report_application where cccd = '081660076239';