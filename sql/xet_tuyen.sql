create or replace procedure create_result_table()
language plpgsql
as $$
    begin
        CREATE TABLE IF NOT EXISTS ket_qua_xet_tuyen (
            ma_nganh  VARCHAR(20) NOT NULL,
            cccd      VARCHAR(12) NOT NULL,
            score     NUMERIC     NOT NULL,
            PRIMARY KEY (ma_nganh, cccd)
        );

        CREATE INDEX IF NOT EXISTS kqxt_ma_nganh_score_idx
            ON ket_qua_xet_tuyen (ma_nganh, score DESC);
    end;
$$;

CREATE OR REPLACE PROCEDURE create_queue_table()
LANGUAGE plpgsql
AS $$
BEGIN
    DROP TABLE IF EXISTS queue;
    CREATE TABLE queue (
        id SERIAL PRIMARY KEY,
        cccd VARCHAR(12) NOT NULL,
        da_xet INT DEFAULT 0,
        trang_thai BOOLEAN DEFAULT FALSE
    );
END $$;

create or replace procedure insert_data()
language plpgsql
as $$
declare
    r record;
    sql text;
    reccccd varchar(12);
    recso_nguyen_vong int;
    recda_xet int;
begin
    for r in select * from nguyen_vong_xet_tuyen loop
        reccccd := r.cccd;
        recda_xet = 0;
        sql := format('INSERT INTO queue (cccd, da_xet) VALUES (%L, %L);',
                      reccccd,
                      recda_xet);

        execute sql;
    end loop;
end;
$$;

/*-----------------------------------------------------------
  2.  Thủ tục xét tuyển batch-mode
-----------------------------------------------------------*/
CREATE OR REPLACE PROCEDURE run_xet_tuyen_batch()
LANGUAGE plpgsql
AS $$
DECLARE
    v_max_nv INT := (
        SELECT MAX(thu_tu_nguyen_vong) FROM nguyen_vong_xet_tuyen
    );
    v_round  INT := 1;
BEGIN
    ----------------------------------------------------------------
    -- 0.  Reset bảng tạm kết quả cho lần chạy mới
    ----------------------------------------------------------------
    TRUNCATE ket_qua_xet_tuyen;

    ----------------------------------------------------------------
    -- 1.  Vòng xét từng nguyện vọng (1 … v_max_nv)
    ----------------------------------------------------------------
    WHILE v_round <= v_max_nv LOOP
        WITH
        /* 1️⃣ Ứng viên vòng hiện tại (chưa đỗ) */
        ung_vien AS (
            SELECT q.cccd,
                   n.ma_nganh,
                   h.diem_xet_tuyen
            FROM   queue q
            JOIN   nguyen_vong_xet_tuyen n USING (cccd)
            JOIN   ho_so_xet_tuyen       h USING (cccd)
            WHERE  q.trang_thai = FALSE
              AND  n.thu_tu_nguyen_vong = v_round
        ),

        /* 2️⃣ Hợp nhất & khử trùng (giữ điểm cao nhất mỗi (ngành, cccd)) */
        hop_ung_vien AS (
            SELECT DISTINCT ON (ma_nganh, cccd)
                   ma_nganh, cccd, score
            FROM (
                SELECT ma_nganh, cccd, score          FROM ket_qua_xet_tuyen
                UNION ALL
                SELECT ma_nganh, cccd, diem_xet_tuyen FROM ung_vien
            ) AS u
            ORDER BY ma_nganh, cccd, score DESC
        ),

        /* 3️⃣ Xếp hạng theo điểm cho từng ngành */
        xep_hang AS (
            SELECT h.*,
                   d.chi_tieu_tuyen_sinh,
                   ROW_NUMBER() OVER (PARTITION BY h.ma_nganh
                                      ORDER BY h.score DESC, h.cccd) AS rn
            FROM   hop_ung_vien h
            JOIN   nganh_dao_tao_dai_hoc d USING (ma_nganh)
        ),

        /* 4️⃣ Danh sách chính thức (top-K) */
        keep AS (
            SELECT * FROM xep_hang
            WHERE  rn <= chi_tieu_tuyen_sinh
        ),

        /* 5️⃣ Thí sinh CẦN CHÈN (mới đỗ) */
        to_insert AS (
            SELECT k.ma_nganh, k.cccd, k.score
            FROM   keep k
            LEFT   JOIN ket_qua_xet_tuyen old
                   USING (ma_nganh, cccd)
            WHERE  old.cccd IS NULL
        ),

        /* 6️⃣ Thí sinh CẦN XOÁ (bị đẩy ra) */
        to_delete AS (
            SELECT old.ma_nganh, old.cccd
            FROM   ket_qua_xet_tuyen old
            LEFT   JOIN keep k
                   USING (ma_nganh, cccd)
            WHERE  k.cccd IS NULL
        ),

        /* 7️⃣ Thao tác chèn, xoá và cập-nhật queue — TẤT CẢ trong CÙNG statement */
        ins AS (
            INSERT INTO ket_qua_xet_tuyen (ma_nganh, cccd, score)
            SELECT * FROM to_insert
            RETURNING cccd
        ),
        del AS (
            DELETE FROM ket_qua_xet_tuyen k
            USING  to_delete d
            WHERE  k.ma_nganh = d.ma_nganh
              AND  k.cccd     = d.cccd
            RETURNING k.cccd
        )
        /* 8️⃣ Cập nhật trạng thái queue cho cả ins & del */
        UPDATE queue q
        SET    trang_thai = CASE
                              WHEN ins.cccd IS NOT NULL THEN TRUE   -- vừa đỗ
                              WHEN del.cccd IS NOT NULL THEN FALSE  -- bị đẩy
                              ELSE q.trang_thai
                            END,
               da_xet     = v_round
        FROM   ins
        FULL   JOIN del USING (cccd)
        WHERE  q.cccd = COALESCE(ins.cccd, del.cccd)
        ;

        /* 9️⃣ Thí sinh rớt vòng này (không đỗ, không bị đẩy) */
        UPDATE queue
        SET    da_xet = v_round
        WHERE  trang_thai = FALSE
          AND  da_xet     < v_round;

        v_round := v_round + 1;
    END LOOP;

END $$;
-- call run_xet_tuyen_batch();

create or replace procedure insert_xet_tuyen_data_into_danh_sach_du_dieu_kien()
language plpgsql
as $$
begin
    INSERT INTO danh_sach_du_dieu_kien_trung_tuyen
        (ma_nganh, ma_truong, cccd, diem_xet_tuyen)
    SELECT  k.ma_nganh,
            d.ma_truong_khoa,        -- 🔸 cột bổ sung
            k.cccd,
            k.score
    FROM    ket_qua_xet_tuyen k
    JOIN    nganh_dao_tao_dai_hoc d USING (ma_nganh);
end;
$$;

select * from danh_sach_du_dieu_kien_trung_tuyen;

-- call clear_danh_sach_du_dieu_kien();

select * from ket_qua_xet_tuyen;



-- select * from queue where trang_thai = false;
CREATE OR REPLACE FUNCTION fn_kiem_tra_rot_oan()
RETURNS TABLE (
    cccd            VARCHAR(12),
    ma_nganh        VARCHAR(20),
    diem_thi_sinh   NUMERIC,
    diem_chuan_nganh NUMERIC
)
LANGUAGE sql
AS $$
WITH
diem_chuan AS (                          -- 1. điểm thấp nhất đang đỗ
    SELECT ma_nganh, MIN(score) AS min_score
    FROM   ket_qua_xet_tuyen
    GROUP  BY ma_nganh
),
next_nv AS (                             -- 2. nguyện vọng kế của thí sinh rớt
    SELECT q.cccd,
           n.ma_nganh
    FROM   queue q
    JOIN   nguyen_vong_xet_tuyen n
           ON n.cccd = q.cccd
          AND n.thu_tu_nguyen_vong = q.da_xet + 1
    WHERE  q.trang_thai = FALSE
)
SELECT nv.cccd,
       nv.ma_nganh,
       h.diem_xet_tuyen  AS diem_thi_sinh,
       dc.min_score      AS diem_chuan_nganh
FROM   next_nv  nv
JOIN   ho_so_xet_tuyen h USING (cccd)
JOIN   diem_chuan      dc USING (ma_nganh)
WHERE  h.diem_xet_tuyen > dc.min_score     -- 3. cao hơn chuẩn
ORDER  BY nv.ma_nganh, h.diem_xet_tuyen DESC;
$$;
SELECT * FROM fn_kiem_tra_rot_oan();
SELECT ma_nganh, COUNT(*) AS so_duoc_nhan, chi_tieu_tuyen_sinh
FROM   danh_sach_du_dieu_kien_trung_tuyen
JOIN   nganh_dao_tao_dai_hoc USING (ma_nganh)
GROUP  BY ma_nganh, chi_tieu_tuyen_sinh
HAVING COUNT(*) > chi_tieu_tuyen_sinh;
CREATE OR REPLACE PROCEDURE xet_tuyen()
LANGUAGE plpgsql
AS $$
DECLARE
    v_rot_oan  INT;
    v_vuot_ct  INT;
    v_trung_pk INT;
BEGIN
    ----------------------------------------------------------------
    -- 1. Chuẩn bị bảng tạm
    ----------------------------------------------------------------
    CALL create_result_table();   -- chỉ tạo 1 lần nếu chưa có
    CALL create_queue_table();
    CALL insert_data();           -- nạp dữ liệu queue

    ----------------------------------------------------------------
    -- 2. Chạy xét tuyển
    ----------------------------------------------------------------
    CALL run_xet_tuyen_batch();

    ----------------------------------------------------------------
    -- 3. Kiểm tra toàn vẹn
    ----------------------------------------------------------------
    /* 3.1 Rớt oan? */
    SELECT COUNT(*) INTO v_rot_oan FROM fn_kiem_tra_rot_oan();
    IF v_rot_oan > 0 THEN
        RAISE EXCEPTION
          'Phát hiện % thí sinh rớt nhưng điểm cao hơn điểm chuẩn ngành. Thuật toán cần rà soát.',
          v_rot_oan;
    END IF;

    /* 3.2 Vượt chỉ tiêu ngành? */
    SELECT COUNT(*) INTO v_vuot_ct
    FROM (
        SELECT ma_nganh
        FROM   ket_qua_xet_tuyen k
        JOIN   nganh_dao_tao_dai_hoc d USING (ma_nganh)
        GROUP  BY ma_nganh, chi_tieu_tuyen_sinh
        HAVING COUNT(*) > chi_tieu_tuyen_sinh
    ) AS t;
    IF v_vuot_ct > 0 THEN
        RAISE EXCEPTION
          'Có % ngành vượt quá chỉ tiêu sau khi xét tuyển.', v_vuot_ct;
    END IF;
    ----------------------------------------------------------------
    -- 4. Ghi dữ liệu sang bảng công bố
    ----------------------------------------------------------------
    TRUNCATE danh_sach_du_dieu_kien_trung_tuyen;

    call insert_xet_tuyen_data_into_danh_sach_du_dieu_kien();

    ----------------------------------------------------------------
    -- 5. Dọn bảng tạm
    ----------------------------------------------------------------
--     DROP TABLE IF EXISTS queue;
--     DROP TABLE IF EXISTS ket_qua_xet_tuyen;

    RAISE NOTICE 'Xét tuyển hoàn tất và đã cập nhật bảng danh_sach_du_dieu_kien_trung_tuyen.';
END;
$$;

call xet_tuyen();

select * from ket_qua_xet_tuyen where cccd = '123456789012';

select * from danh_sach_du_dieu_kien_trung_tuyen;

select * from danh_sach_du_dieu_kien_trung_tuyen where ma_nganh = 'QST7480107';

create or replace function truy_van_ket_qua_xet_tuyen(
    p_cccd varchar(12)
)
returns table (
    trang_thai boolean,
    ma_nganh varchar(20),
    diem_xet_tuyen numeric
)
language sql
as $$
    with
    ds AS (
        select cccd, ma_nganh, diem_xet_tuyen
        from danh_sach_du_dieu_kien_trung_tuyen
        where cccd = p_cccd
    )
    select case when exists (select * from ds) then true else false end as trang_thai,
           ma_nganh,
           diem_xet_tuyen
    from ds
    union all
    select false, null, null
    where not exists (select * from ds);

$$;

select * from truy_van_ket_qua_xet_tuyen('123456789012');

create or replace function diem_chuan_nganh(
    p_ma_nganh varchar(20)
)
returns numeric
language sql
as $$
    select min(score)
    from ket_qua_xet_tuyen
    where ma_nganh = p_ma_nganh;
$$;

select diem_chuan_nganh('QST7480107');