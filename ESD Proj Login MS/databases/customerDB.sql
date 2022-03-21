create schema customerDB;
use customerDB;

create table customer(
customer_id int,
name varchar(40),
email varchar(40),
constraint customer_pk primary key (customer_id)
);
insert into customer values(1, 'may', 'may@gmail.com');
GRANT REFERENCES ON customerDB.customer TO loginDB;