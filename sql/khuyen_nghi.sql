CREATE OR REPLACE FUNCTION fn_khuyen_nghi_nganh_hoc(
  p_cccd VARCHAR
)
RETURNS TABLE(
  cccd               CHAR(12),
  ma_nganh           VARCHAR(30),
  ten_nganh          VARCHAR(100),
  thu_tu_khuyen_nghi INT,
  diem_chuan_nam_truoc INT
)
LANGUAGE plpgsql
AS $$
DECLARE
  v_kn1 INT; v_kn2 INT; v_kn3 INT; v_kn4 INT; v_kn5 INT;
  v_diem_thi NUMERIC;
  v_threshold NUMERIC := 100;
  top_skills_4 TEXT[];
  top_skills_3 TEXT[];
BEGIN
  -- 1) Lấy đánh giá kỹ năng & điểm thi cao nhất
  SELECT
    tks.danh_gia_ky_nang_tieng_viet,
    tks.danh_gia_ky_nang_tieng_anh,
    tks.danh_gia_ky_nang_toan_hoc,
    tks.danh_gia_ky_nang_logic_phan_tich_so_lieu,
    tks.danh_gia_ky_nang_suy_luan_khoa_hoc,
    tks.diem_thi_cao_nhat
  INTO
    v_kn1, v_kn2, v_kn3, v_kn4, v_kn5, v_diem_thi
  FROM ky_nang_cua_thi_sinh AS tks
  WHERE tks.cccd = p_cccd;

  -- 2) Mảng 4 kỹ năng cao nhất (vòng 2)
  SELECT array_agg(skill) INTO top_skills_4
  FROM (
    SELECT skill
    FROM (VALUES
      ('kn1', v_kn1), ('kn2', v_kn2),
      ('kn3', v_kn3), ('kn4', v_kn4),
      ('kn5', v_kn5)
    ) AS s(skill, rating)
    ORDER BY rating DESC, random()
    LIMIT 4
  ) sub;

  -- 3) Mảng 3 kỹ năng cao nhất (vòng 3)
  SELECT array_agg(skill) INTO top_skills_3
  FROM (
    SELECT skill
    FROM (VALUES
      ('kn1', v_kn1), ('kn2', v_kn2),
      ('kn3', v_kn3), ('kn4', v_kn4),
      ('kn5', v_kn5)
    ) AS s(skill, rating)
    ORDER BY rating DESC, random()
    LIMIT 3
  ) sub;

  -- 4) Chọn 5 ứng viên theo priority rồi sắp xếp lại theo diem_chuan DESC
  RETURN QUERY
  WITH
  t1 AS (
    SELECT nd.ma_nganh, nd.ten_nganh, nd.diem_chuan_nam_truoc, 1 AS priority
    FROM nganh_dao_tao_dai_hoc AS nd
    WHERE
      nd.ky_nang_tieng_viet              = v_kn1
      AND nd.ky_nang_tieng_anh           = v_kn2
      AND nd.ky_nang_toan_hoc            = v_kn3
      AND nd.ky_nang_logic_phan_tich_so_lieu = v_kn4
      AND nd.ky_nang_suy_luan_khoa_hoc   = v_kn5
      AND nd.diem_chuan_nam_truoc    <= v_diem_thi
      AND (v_diem_thi - nd.diem_chuan_nam_truoc) <= v_threshold
  ),
  t2 AS (
    SELECT nd.ma_nganh, nd.ten_nganh, nd.diem_chuan_nam_truoc, 2 AS priority
    FROM nganh_dao_tao_dai_hoc AS nd
    WHERE
      nd.diem_chuan_nam_truoc    <= v_diem_thi
      AND (v_diem_thi - nd.diem_chuan_nam_truoc) <= v_threshold
      AND (
        (CASE WHEN 'kn1' = ANY(top_skills_4) AND nd.ky_nang_tieng_viet              = v_kn1 THEN 1 ELSE 0 END) +
        (CASE WHEN 'kn2' = ANY(top_skills_4) AND nd.ky_nang_tieng_anh           = v_kn2 THEN 1 ELSE 0 END) +
        (CASE WHEN 'kn3' = ANY(top_skills_4) AND nd.ky_nang_toan_hoc            = v_kn3 THEN 1 ELSE 0 END) +
        (CASE WHEN 'kn4' = ANY(top_skills_4) AND nd.ky_nang_logic_phan_tich_so_lieu = v_kn4 THEN 1 ELSE 0 END) +
        (CASE WHEN 'kn5' = ANY(top_skills_4) AND nd.ky_nang_suy_luan_khoa_hoc   = v_kn5 THEN 1 ELSE 0 END)
      ) >= 4
  ),
  t3 AS (
    SELECT nd.ma_nganh, nd.ten_nganh, nd.diem_chuan_nam_truoc, 3 AS priority
    FROM nganh_dao_tao_dai_hoc AS nd
    WHERE
      nd.diem_chuan_nam_truoc    <= v_diem_thi
      AND (v_diem_thi - nd.diem_chuan_nam_truoc) <= v_threshold
      AND (
        (CASE WHEN 'kn1' = ANY(top_skills_3) AND nd.ky_nang_tieng_viet              = v_kn1 THEN 1 ELSE 0 END) +
        (CASE WHEN 'kn2' = ANY(top_skills_3) AND nd.ky_nang_tieng_anh           = v_kn2 THEN 1 ELSE 0 END) +
        (CASE WHEN 'kn3' = ANY(top_skills_3) AND nd.ky_nang_toan_hoc            = v_kn3 THEN 1 ELSE 0 END) +
        (CASE WHEN 'kn4' = ANY(top_skills_3) AND nd.ky_nang_logic_phan_tich_so_lieu = v_kn4 THEN 1 ELSE 0 END) +
        (CASE WHEN 'kn5' = ANY(top_skills_3) AND nd.ky_nang_suy_luan_khoa_hoc   = v_kn5 THEN 1 ELSE 0 END)
      ) >= 3
  ),
  t4 AS (
    SELECT nd.ma_nganh, nd.ten_nganh, nd.diem_chuan_nam_truoc, 4 AS priority
    FROM nganh_dao_tao_dai_hoc AS nd
    WHERE
      nd.diem_chuan_nam_truoc    <= v_diem_thi
      AND (v_diem_thi - nd.diem_chuan_nam_truoc) <= v_threshold
  ),
  all_candidates AS (
    SELECT * FROM t1
    UNION ALL
    SELECT * FROM t2
    UNION ALL
    SELECT * FROM t3
    UNION ALL

    SELECT * FROM t4
  ),
  picked AS (
    -- Lấy 5 ứng viên đầu theo priority
    SELECT *
    FROM all_candidates
    ORDER BY priority, random()
    LIMIT 5
  )
  -- Sau đó sắp xếp lại 5 ứng viên đó theo diem_chuan DESC
  SELECT
    p_cccd::char(12)                                               AS cccd,
    pk.ma_nganh,
    pk.ten_nganh,
    (ROW_NUMBER() OVER (ORDER BY pk.diem_chuan_nam_truoc DESC))::INT AS thu_tu_khuyen_nghi,
    pk.diem_chuan_nam_truoc
  FROM picked AS pk
  ORDER BY pk.diem_chuan_nam_truoc DESC;
END;
$$;



SELECT * FROM fn_khuyen_nghi_nganh_hoc('075128409260');
SELECT * FROM fn_khuyen_nghi_nganh_hoc('039701800911');
SELECT * FROM fn_khuyen_nghi_nganh_hoc('034305789630');
