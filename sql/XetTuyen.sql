CREATE OR REPLACE PROCEDURE create_sorted_tables()
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
    sql TEXT;
    ind TEXT;
BEGIN
    FOR r IN SELECT ma_nganh FROM nganh_dao_tao_dai_hoc LOOP

        sql := format('CREATE TABLE IF NOT EXISTS %I (id SERIAL PRIMARY KEY, cccd varchar(12) NOT NULL, score numeric)', r.ma_nganh);
        EXECUTE sql;
        ind := format('CREATE INDEX IF NOT EXISTS %I ON %I (score DESC);',
              r.ma_nganh || '_idx',
              r.ma_nganh);
        EXECUTE ind;

    END LOOP;
END $$;

call create_sorted_tables();

-- SELECT * FROM "QSX7140114";

-- insert into "QSX7140114" (cccd, score) values ('123456789012', 600);
-- insert into "QSX7140114" (cccd, score) values ('123456789013', 750);
-- insert into "QSX7140114" (cccd, score) values ('123456789014', 700);
--
-- DO $$
--     DECLARE lowest varchar(12);
--     begin
--         SELECT cccd INTO lowest FROM "QSX7140114" ORDER BY score DESC LIMIT 1;
--         -- print lowest
--         RAISE NOTICE 'Lowest score: %', lowest;
--     end;
--     $$


CREATE OR REPLACE PROCEDURE drop_sorted_tables()
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
    sql TEXT;
BEGIN
    FOR r IN SELECT ma_nganh FROM nganh_dao_tao_dai_hoc LOOP
        sql := format('DROP TABLE IF EXISTS %I;', r.ma_nganh);
        EXECUTE sql;
    END LOOP;
END $$;

call drop_sorted_tables();

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


select * from queue;

-- CREATE OR REPLACE FUNCTION check_stop_condition()
-- RETURNS BOOLEAN
-- LANGUAGE plpgsql
-- AS $$
-- DECLARE
--     total_count INT;
--     valid_count INT;
-- BEGIN
--     SELECT COUNT(*) INTO total_count FROM queue;
--
--     SELECT COUNT(*) INTO valid_count
--     FROM queue
--     WHERE trang_thai = TRUE
--        OR (trang_thai = FALSE AND so_nguyen_vong = da_xet);
--
--     RETURN valid_count = total_count;
-- END $$;
--
-- -- remove function check_stop_condition
-- drop function if exists check_stop_condition;
--

drop table if exists queue;

-- insert into queue (cccd, so_nguyen_vong, da_xet) values ('123456789012', 1, 1);
-- insert into queue (cccd, so_nguyen_vong, da_xet, trang_thai) values ('123456789013', 2, 1, true);
-- insert into queue (cccd, so_nguyen_vong, da_xet) values ('123456789014', 3, 2);
--
-- select check_stop_condition();

select * from nguyen_vong_xet_tuyen limit 1;

call create_sorted_tables();
call create_queue_table();

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

call insert_data();

select * from queue;

create or replace view cccd_temp as select cccd from queue where trang_thai = false;
select * from cccd_temp;
drop view cccd_temp;

CREATE OR REPLACE PROCEDURE run_xet_tuyen_queue()
language plpgsql
AS $$
declare
    r  record;
    complete_student int;
    total_student int;

    current_cccd varchar(12);
    current_so_nguyen_vong int;
    current_da_xet int;

    current_ma_nganh varchar(20);
    current_diem_xet_tuyen int;

    current_nganh_soluong int;
    current_nganh_chitieu int;

    last_cccd varchar(12);
    last_diem_xt int;
    sql text;
begin
    total_student := (select count(*) from queue);
    complete_student := 0;

    while complete_student < total_student loop
        create or replace view cccd_to_process as select cccd from queue where trang_thai = false ;
        for r in select * from cccd_to_process loop
                current_cccd := r.cccd;
                select so_nguyen_vong, da_xet into current_so_nguyen_vong, current_da_xet from queue where cccd = current_cccd;
                if current_da_xet >= current_so_nguyen_vong then
                    update queue set trang_thai = true where cccd = current_cccd;
                    complete_student := complete_student + 1;
                    continue;
                end if;
                select ma_nganh into current_ma_nganh from nguyen_vong_xet_tuyen where cccd = current_cccd and thu_tu_nguyen_vong = current_da_xet + 1;
                if current_ma_nganh is null then
                    continue ;
                end if;
                select ho_so_xet_tuyen.diem_xet_tuyen into current_diem_xet_tuyen from ho_so_xet_tuyen where cccd = current_cccd ;
                if current_diem_xet_tuyen is null then
                    continue ;
                end if;
                select nganh_dao_tao_dai_hoc.chi_tieu_tuyen_sinh into current_nganh_chitieu from nganh_dao_tao_dai_hoc where ma_nganh = current_ma_nganh;
                select count(*) into current_nganh_soluong from format('%I', current_ma_nganh);
                if current_nganh_soluong < current_nganh_chitieu then
                    sql := format('INSERT INTO %I (cccd, score) VALUES (%L, %L);',
                                  current_ma_nganh,
                                  current_cccd,
                                  current_diem_xet_tuyen);
                    execute sql;
                    complete_student := complete_student + 1;
                    update queue set trang_thai = true where cccd = current_cccd;
                    update queue set da_xet = da_xet + 1 where cccd = current_cccd;
                else
                    select cccd, score into last_cccd, last_diem_xt from format('%I', current_ma_nganh) order by score desc limit 1;
                    if last_diem_xt < current_diem_xet_tuyen then
                        sql := format('DELETE FROM %I WHERE cccd = %L;', current_ma_nganh, last_cccd);
                        execute sql;

                        sql := format('INSERT INTO %I (cccd, score) VALUES (%L, %L);',
                                      current_ma_nganh,
                                      current_cccd,
                                      current_diem_xet_tuyen);
                        execute sql;
                        update queue set trang_thai = false where cccd = last_cccd;
                        update queue set da_xet = da_xet + 1 where cccd = last_cccd;

                        update queue set trang_thai = true where cccd = current_cccd;
                        update queue set da_xet = da_xet + 1 where cccd = current_cccd;

                    else
                        continue ;
                    end if;
                end if;

            end loop;
        end loop;
    end;

    $$;

call drop_sorted_tables();
call create_sorted_tables();

select * from "QSA7140201";
select * from queue;