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
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
    current_cccd varchar(12);
    current_so_nguyen_vong int;
    current_da_xet int;
    current_ma_nganh varchar(20);
    current_diem_xet_tuyen int;
    current_nganh_soluong int;
    current_nganh_chitieu int;
    last_cccd varchar(12);
    last_diem_xt numeric;
    sql text;

    changes_made BOOLEAN := TRUE;
    loop_counter INT := 0;
BEGIN
    WHILE changes_made AND loop_counter < 10000 LOOP
        loop_counter := loop_counter + 1;
        changes_made := FALSE;

        FOR r IN SELECT cccd FROM queue WHERE trang_thai = FALSE LOOP
            current_cccd := r.cccd;

            SELECT so_nguyen_vong, da_xet INTO current_so_nguyen_vong, current_da_xet FROM queue WHERE cccd = current_cccd;

            IF current_da_xet >= current_so_nguyen_vong THEN
                UPDATE queue SET trang_thai = TRUE WHERE cccd = current_cccd;
                changes_made := TRUE;
                CONTINUE;
            END IF;

            SELECT ma_nganh INTO current_ma_nganh FROM nguyen_vong_xet_tuyen
                WHERE cccd = current_cccd AND thu_tu_nguyen_vong = current_da_xet + 1;

            IF current_ma_nganh IS NULL THEN
                UPDATE queue SET da_xet = da_xet + 1 WHERE cccd = current_cccd;
                changes_made := TRUE;
                CONTINUE;
            END IF;

            SELECT diem_xet_tuyen INTO current_diem_xet_tuyen FROM ho_so_xet_tuyen WHERE cccd = current_cccd;

            IF current_diem_xet_tuyen IS NULL THEN
                UPDATE queue SET trang_thai = TRUE WHERE cccd = current_cccd;
                changes_made := TRUE;
                CONTINUE;
            END IF;

            SELECT chi_tieu_tuyen_sinh INTO current_nganh_chitieu FROM nganh_dao_tao_dai_hoc WHERE ma_nganh = current_ma_nganh;

            EXECUTE format('SELECT COUNT(*) FROM %I', current_ma_nganh) INTO current_nganh_soluong;

            IF current_nganh_soluong < current_nganh_chitieu THEN
                sql := format('INSERT INTO %I (cccd, score) VALUES (%L, %L);',
                              current_ma_nganh, current_cccd, current_diem_xet_tuyen);
                EXECUTE sql;

                UPDATE queue SET trang_thai = TRUE, da_xet = da_xet + 1 WHERE cccd = current_cccd;
                changes_made := TRUE;
            ELSE
                EXECUTE format('SELECT cccd, score FROM %I ORDER BY score ASC LIMIT 1;', current_ma_nganh) INTO last_cccd, last_diem_xt;

                IF last_diem_xt < current_diem_xet_tuyen THEN
                    EXECUTE format('DELETE FROM %I WHERE cccd = %L;', current_ma_nganh, last_cccd);

                    sql := format('INSERT INTO %I (cccd, score) VALUES (%L, %L);',
                                  current_ma_nganh, current_cccd, current_diem_xet_tuyen);
                    EXECUTE sql;

                    UPDATE queue SET trang_thai = FALSE, da_xet = da_xet + 1 WHERE cccd = last_cccd;
                    UPDATE queue SET trang_thai = TRUE, da_xet = da_xet + 1 WHERE cccd = current_cccd;

                    changes_made := TRUE;
                ELSE
                    UPDATE queue SET da_xet = da_xet + 1 WHERE cccd = current_cccd;
                    changes_made := TRUE;
                END IF;
            END IF;
        END LOOP;
    END LOOP;

    IF loop_counter = 10000 THEN
        RAISE NOTICE 'Procedure terminated after maximum loops reached (10000 iterations). Check logic!';
    END IF;

END;
$$;
call drop_sorted_tables();
call create_sorted_tables();

select * from "QSA7140201";
select * from queue;

create index if not exists queue_idx on queue (cccd);
call run_xet_tuyen_queue();

call drop_sorted_tables();

create or replace procedure clear_queue()
language plpgsql
as $$
declare
    r record;
    sql text;
begin
    for r in select * from queue loop
        sql := format('DELETE FROM queue WHERE cccd = %L;', r.cccd);
        execute sql;
    end loop;
end;
$$;
call clear_queue();
select * from queue;

call insert_data();

-- create index if not exists queue_idx on queue (cccd);
