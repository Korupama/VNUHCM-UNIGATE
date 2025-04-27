-- alter table tai_khoan_thi_sinh alter column mat_khau TYPE varchar(255);
--
-- select * from tai_khoan_thi_sinh;
--

CREATE EXTENSION IF NOT EXISTS pgcrypto;

create or replace procedure encrypt_password()
language plpgsql
as $$
declare
    r record;
begin
    for r in select * from tai_khoan_thi_sinh loop
        update tai_khoan_thi_sinh
        set mat_khau = crypt(r.mat_khau, gen_salt('bf'))
        where cccd = r.cccd;
    end loop;
end;
$$;

call encrypt_password();

select * from tai_khoan_thi_sinh;

create or replace procedure insert_tai_khoan(
    p_cccd varchar(12),
    p_mat_khau varchar(255)
)
language plpgsql
as $$
declare
    r record;
    sql text;
begin
    select * into r from tai_khoan_thi_sinh where cccd = p_cccd;
    if not found then
        sql := format('INSERT INTO tai_khoan_thi_sinh (cccd, mat_khau) VALUES (%L, %L);',
                      p_cccd,
                      crypt(p_mat_khau, gen_salt('bf')));
        execute sql;
    else
        raise notice 'Tai khoan da ton tai';
    end if;
end;
$$;

-- call insert_tai_khoan('093312181033', '123');
create or replace function check_password(
    p_cccd varchar(12),
    p_mat_khau varchar(255)
)
returns boolean
language plpgsql
as $$
declare
    r record;
    sql text;
    is_valid boolean;
begin
    select * into r from tai_khoan_thi_sinh where cccd = p_cccd;
    if not found then
        raise notice 'Tai khoan khong ton tai';
        return false;
    else
        sql := format('SELECT crypt(%L, mat_khau) = mat_khau FROM tai_khoan_thi_sinh WHERE cccd = %L;',
                      p_mat_khau,
                      p_cccd);
        execute sql into is_valid;
        return is_valid;
    end if;
end;
$$;

select check_password('022751590918','doxbe')

select * from tai_khoan_thi_sinh;

create or replace procedure update_password(
    p_cccd varchar(12),
    p_mat_khau varchar(255)
)
language plpgsql
as $$
declare
    r record;
begin
    for r in select * from tai_khoan_thi_sinh where cccd = p_cccd loop
        if not found then
            raise notice 'Tai khoan khong ton tai';
        end if;
    end loop;
    update tai_khoan_thi_sinh set mat_khau = crypt(p_mat_khau, gen_salt('bf'))
    where cccd = p_cccd;
end;
$$;

call update_password('022751590918','doanduyenmy13');

select check_password('022751590918','doanduyenmy13');

create or replace procedure remove_tai_khoan(
    p_cccd varchar(12)
)
language plpgsql
as $$
declare
    r record;
    sql text;
begin
    select * into r from tai_khoan_thi_sinh where cccd = p_cccd;
    if not found then
        raise notice 'Tai khoan khong ton tai';
    else
        sql := format('DELETE FROM tai_khoan_thi_sinh WHERE cccd = %L;', p_cccd);
        execute sql;
    end if;
end;
$$;

-- select check_password('abc', 'xyz')

-- select * from tai_khoan_thi_sinh where cccd='064205014073';