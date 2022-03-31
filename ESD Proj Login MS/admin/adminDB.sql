create schema adminDB;
use adminDB;

create table admin(
admin_id int auto_increment,
name varchar(40),
email varchar(40),
constraint admin_pk primary key(admin_id)
);

insert into admin(name, email) values('jun', 'jun@gmail.com');
GRANT REFERENCES ON adminDB.admin TO loginDB;-- 