drop table if exists cvs;
create table cvs (
    id integer primary key autoincrement,
    username text,
    name text,
    age integer,
    education text,
    work_experience text,
    skills text,
    email text,
    telephone integer
);