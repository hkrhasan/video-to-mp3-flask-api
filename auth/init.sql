CREATE USER 'hkr'@'localhost' IDENTIFIED BY 'P@ssw0rd';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* TO 'hkr'@'localhost';

USE auth;

CREATE TABLE user (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('hkr@gmail.com', 'P@ssw0rd');