create schema loginDB;
use loginDB;

create table login(
username varchar(20),
password varchar(20),
customer_id int,
admin_id int,
constraint login_pk PRIMARY KEY (username),
constraint login_fk1 foreign key (customer_id) references customerDB.customer (customer_id),
constraint login_fk2 foreign key (admin_id) references adminDB.admin (admin_id)
);

insert into login(username, password, admin_id) values('dumpling', 'password', '1');
insert into login(username, password, customer_id) values('may', 'password', '1');