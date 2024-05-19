CREATE DATABASE IF NOT EXISTS token_auth;
USE token_auth;

CREATE TABLE IF NOT EXISTS `users` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `role` varchar(10) DEFAULT NULL
);

CREATE USER 'user'@'localhost' IDENTIFIED BY '25CdBXS3ACGCnZ4sPTvTV8hJ';
GRANT ALL PRIVILEGES ON token_auth.* TO 'user'@'localhost';
FLUSH PRIVILEGES;
