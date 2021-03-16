DROP TABLE IF EXISTS Users
DROP TABLE IF EXISTS Inventory
DROP TABLE IF EXISTS Category 
DROP TABLE IF EXISTS Product
DROP TABLE IF EXISTS Attribute

-- create the tables

CREATE TABLE Users (
    user_id BIGSERIAL PRIMARY KEY,
    user_nm VARCHAR(30) NOT NULL,
    email VARCHAR(50)
);

CREATE TABLE Inventory (
    inventory_id BIGSERIAL PRIMARY KEY,
    user_id INT REFERENCES Users (user_id),
    inventory_nm VARCHAR(30) NOT NULL,
    created_at DATETIME NOT NULL
);

CREATE TABLE Category (
    category_id BIGSERIAL PRIMARY KEY,
    inventory_id INT REFERENCES Inventory (inventory_id),
    category_nm VARCHAR(30) NOT NULL,
    created_at DATETIME NOT NULL
);

CREATE TABLE Product (
    product_id BIGSERIAL PRIMARY KEY,
    category_id INT REFERENCES Category (category_id),
    product_nm VARCHAR(80) NOT NULL,
    product_type VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    last_addition DATETIME NOT NULL,
    last_removal DATETIME NOT NULL,
    created_at DATETIME NOT NULL
);

CREATE TABLE Attribute (
    attribute_id BIGSERIAL PRIMARY KEY,
    product_id INT REFERENCES Product (product_id),
    attr_nm VARCHAR(MAX) NOT NULL,
    attr_value VARCHAR(MAX) NOT NULL
);