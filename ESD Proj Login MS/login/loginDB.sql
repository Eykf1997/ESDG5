create schema loginDB;
use loginDB;

create table login(
username varchar(20),
password varchar(20),
account_type varchar(2),
customer_id int,
admin_id int,
constraint login_pk PRIMARY KEY (username),
constraint login_fk1 foreign key (customer_id) references customerDB.customer (customer_id),
constraint login_fk2 foreign key (admin_id) references adminDB.admin (admin_id)
);

-- insert into login(username, password, account_type, customer_id) values('dumpling', 'password', 'ad', '1');
-- select * from login l inner join customerdb.customer c on l.customer_id = c.customer_id;