CREATE DATABASE desafio_final;

USE desafio_final;

CREATE TABLE tb_clients(
id int not null,
nome varchar(250) not null,
email varchar(250) not null,
data_cadastro datetime not null,
telefone varchar(16),
PRIMARY KEY (id)
);

CREATE TABLE tb_transaction(
id int not null,
client_id int not null,
valor float not null,
data datetime,
PRIMARY KEY (id),
FOREIGN KEY (client_id) REFERENCES tb_clients(id)
);