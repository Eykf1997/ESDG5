create schema customerDB;
use customerDB;

create table customer(
customer_id int auto_increment,
name varchar(40),
email varchar(40),
constraint customer_pk primary key (customer_id)
);
insert into customer(name, email) values('may', 'may@gmail.com');
GRANT REFERENCES ON customerDB.customer TO loginDB;