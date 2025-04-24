CREATE TABLE IF NOT EXISTS ket_qua_xet_tuyen (
    ma_nganh  VARCHAR(20) NOT NULL,
    cccd      VARCHAR(12) NOT NULL,
    score     NUMERIC     NOT NULL,
    PRIMARY KEY (ma_nganh, cccd)
);

CREATE INDEX IF NOT EXISTS kqxt_ma_nganh_score_idx
        ON ket_qua_xet_tuyen (ma_nganh, score DESC);

CREATE OR REPLACE PROCEDURE create_queue_table()
LANGUAGE plpgsql
AS $$
BEGIN
    DROP TABLE IF EXISTS queue;
    CREATE TABLE queue (
        id SERIAL PRIMARY KEY,
        cccd VARCHAR(12) NOT NULL,
        so_nguyen_vong INT NOT NULL,
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
        select count(*) into recso_nguyen_vong from nguyen_vong_xet_tuyen where cccd = r.cccd;
        recda_xet = 0;
        sql := format('INSERT INTO queue (cccd, so_nguyen_vong, da_xet) VALUES (%L, %L, %L);',
                      reccccd,
                      recso_nguyen_vong,
                      recda_xet);

        execute sql;
    end loop;
end;
$$;

call create_queue_table();
call insert_data();

/*-----------------------------------------------------------
  2.  Thủ tục xét tuyển batch-mode
-----------------------------------------------------------*/
CREATE OR REPLACE PROCEDURE run_xet_tuyen_batch()
LANGUAGE plpgsql
AS $$
DECLARE
    v_max_nv  INT := (SELECT MAX(thu_tu_nguyen_vong)
                      FROM   nguyen_vong_xet_tuyen);
    v_round   INT := 1;
BEGIN
    -- Xoá kết quả cũ cho lần chạy mới (tuỳ ý)
    TRUNCATE ket_qua_xet_tuyen;

    WHILE v_round <= v_max_nv LOOP
        ----------------------------------------------------------------
        -- Trong một vòng duy nhất, gói toàn bộ logic vào ONE statement
        ----------------------------------------------------------------
        WITH
        /* 1️⃣  Danh sách ứng viên của vòng v_round */
        ung_vien AS (
            SELECT q.cccd,
                   n.ma_nganh,
                   h.diem_xet_tuyen,
                   d.chi_tieu_tuyen_sinh,
                   ROW_NUMBER() OVER (PARTITION BY n.ma_nganh
                                      ORDER BY h.diem_xet_tuyen DESC) AS rnk
            FROM   queue                 q
            JOIN   nguyen_vong_xet_tuyen n ON n.cccd = q.cccd
            JOIN   ho_so_xet_tuyen       h ON h.cccd = q.cccd
            JOIN   nganh_dao_tao_dai_hoc d USING (ma_nganh)
            WHERE  q.trang_thai = FALSE
              AND  n.thu_tu_nguyen_vong = v_round
        ),
        /* 2️⃣  Giữ lại đúng số chỉ tiêu */
        duoc_nhan AS (
            SELECT *
            FROM   ung_vien
            WHERE  rnk <= chi_tieu_tuyen_sinh
        ),
        /* 3️⃣  Chèn vào bảng kết quả, lấy ra các thí sinh đã đỗ */
        inserted AS (
            INSERT INTO ket_qua_xet_tuyen (ma_nganh, cccd, score)
            SELECT ma_nganh, cccd, diem_xet_tuyen
            FROM   duoc_nhan
            ON CONFLICT (ma_nganh, cccd) DO NOTHING
            RETURNING cccd
        ),
        /* 4️⃣  Đánh dấu queue -> đã trúng tuyển */
        updated_true AS (
            UPDATE queue q
            SET    trang_thai = TRUE,
                   da_xet     = v_round
            FROM   inserted i
            WHERE  q.cccd = i.cccd
            RETURNING q.cccd
        )
        /* 5️⃣  Những thí sinh không đỗ nhưng đã xét xong vòng này */
        UPDATE queue q
        SET    da_xet = v_round
        WHERE  trang_thai = FALSE
          AND  da_xet < v_round;

        ----------------------------------------------------------------
        v_round := v_round + 1;   -- sang vòng nguyện vọng tiếp theo
    END LOOP;
END $$;
call run_xet_tuyen_batch();

select * from ket_qua_xet_tuyen;