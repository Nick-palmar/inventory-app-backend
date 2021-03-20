
-- query to insert test records into the db (so that test data can be refreshed when the schema changes)

INSERT INTO Users(user_nm, email)
VALUES ('nick', 'nicolas.palmar@.com'),
('nick2', 'nicolas.palmar89@.com'),
('nic3', 'nicolas.palmar'), 
('jess', 'j.fajyj@gmail.com'),
('lucas', 'lucas.palmar76@rogers.com'),
('lucas', 'lucas.palmaruj@rogers.com'),
('nick2', 'nicolas.palmar23@.com'),
('nic3', 'nicolas.palmar42r@gmail.com');

INSERT INTO Inventory(user_id, inventory_nm)
VALUES ();

INSERT INTO Category(inventory_id, category_nm)
VALUES ();

INSERT INTO Product(category_id, product_nm, product_type, quantity)
VALUES ();

INSERT INTO Attribute(product_id, attr_nm, attr_value)
VALUES (); 