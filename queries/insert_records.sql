
-- query to insert test records into the db (so that test data can be refreshed when the schema changes)

INSERT INTO Users(user_nm, email)
VALUES ('nick', 'nicolas.palmar@hotmail.com'),
    ('nick2', 'nicolas.palmar89@gmail.com'),
    ('nic3', 'nicolas.palmar2347@gmail.com'), 
    ('jess', 'j.fajyj@gmail.com'),
    ('jess', 'j.fag@outlook.com'),
    ('lucas', 'lucas.palmar76@rogers.com'),
    ('lucas', 'lucas.palma5870j@rogers.com'),
    ('nick2', 'nicolas.palmar23@.com'),
    ('nic3', 'nicolas.palmar42r@gmail.com'),
    ('nancy', 'nancy.lo413@gmail.com'),
    ('nancy2', 'nancy.lo13412@gmail.com'),
    ('oscar', 'oscar.pal82930@gmail.com'),
    ('oscar2', 'oscar.pal90485@gmail.com');

INSERT INTO Inventory(user_id, inventory_nm)
VALUES ();

INSERT INTO Category(inventory_id, category_nm)
VALUES ();

INSERT INTO Product(category_id, product_nm, product_type, quantity)
VALUES ();

INSERT INTO Attribute(product_id, attr_nm, attr_value)
VALUES (); 