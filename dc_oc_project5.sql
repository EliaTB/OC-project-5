CREATE DATABASE openfoodfact;

USE openfoodfact;


CREATE TABLE category(
    id INT NOT NULL AUTO_INCREMENT,
    tag VARCHAR(300) NULL,
    name VARCHAR(300) NOT NULL,
    url VARCHAR(255) NOT NULL,
    CONSTRAINT id PRIMARY KEY (id)
);


CREATE TABLE product(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(300) NOT NULL,
    store VARCHAR(300) NOT NULL,
    nutrition_grade CHAR(1) NOT NULL,
    url VARCHAR(255) NOT NULL,
	category VARCHAR(300) NOT NULL,
    CONSTRAINT id PRIMARY KEY (id)
);


CREATE TABLE favorite(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(300) NOT NULL,
    store VARCHAR(300) NOT NULL,
    nutrition_grade CHAR(1) NOT NULL,
    url VARCHAR(255) NOT NULL,
    category VARCHAR(300) NOT NULL,
    CONSTRAINT id PRIMARY KEY (id)
);


