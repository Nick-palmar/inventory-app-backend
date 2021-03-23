-- drop with backwards order due to foreign key constraints
DROP TABLE IF EXISTS Attribute;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Users;

-- create the tables

CREATE TABLE Users (
    user_id BIGSERIAL PRIMARY KEY,
    user_nm VARCHAR(30) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Inventory (
    inventory_id BIGSERIAL PRIMARY KEY,
    user_id INT REFERENCES Users (user_id) ON DELETE CASCADE,
    inventory_nm VARCHAR(30) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Category (
    category_id BIGSERIAL PRIMARY KEY,
    inventory_id INT REFERENCES Inventory (inventory_id) ON DELETE CASCADE,
    category_nm VARCHAR(30) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Product (
    product_id BIGSERIAL PRIMARY KEY,
    category_id INT REFERENCES Category (category_id) ON DELETE CASCADE,
    product_nm VARCHAR(80) NOT NULL,
    product_type VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    last_addition TIMESTAMP,
    last_removal TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Attribute (
    attribute_id BIGSERIAL PRIMARY KEY,
    product_id INT REFERENCES Product (product_id) ON DELETE CASCADE,
    attr_nm TEXT NOT NULL,
    attr_value TEXT NOT NULL
);