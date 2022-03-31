create schema loginDB2;
use loginDB2;

create table login(
username varchar(20),
password varchar(20),
customer_id int,
admin_id int,
constraint login_pk PRIMARY KEY (username)
)