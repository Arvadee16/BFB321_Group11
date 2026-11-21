
USE my_diners_db;

INSERT INTO kitchen_stations
(kitchen_stations_name, kitchen_stations_workload_limit, kitchen_stations_active)
VALUES
('Grill', 5, 1),
('Curry', 5, 1),
('Bread', 5, 1),
('Dishwashing', 5, 1);


INSERT INTO menu_items
(menu_items_name, kitchen_stations_id, menu_items_price, menu_items_prep_time, menu_items_available)
VALUES
('Chicken Tikka', 1, 95.00, 20, 1),
('Beef Burger', 1, 85.00, 15, 1),
('Chicken Curry', 2, 110.00, 25, 1),
('Lamb Curry', 2, 135.00, 30, 1),
('Garlic Naan', 3, 25.00, 10, 1),
('Butter Naan', 3, 20.00, 10, 1);


INSERT INTO orders
(orders_customer_name, orders_channel, orders_status)
VALUES
('Ahmed', 'Walk-in', 'Received'),
('Kiran', 'Telephone', 'Preparing'),
('Abdur-Rahmaan', 'Delivery', 'Ready'),
('Tebang', 'Walk-in', 'Completed'),
('Jessica', 'Telephone', 'Received');


INSERT INTO order_items
(orders_id, menu_items_id, order_items_quantity, order_items_unit_price, order_items_status)
VALUES
(1, 1, 2, 95.00, 'Received'),
(1, 5, 2, 25.00, 'Received'),
(2, 2, 1, 85.00, 'Preparing'),
(3, 3, 2, 110.00, 'Ready'),
(4, 4, 1, 135.00, 'Completed'),
(4, 6, 2, 20.00, 'Completed'),
(5, 1, 1, 95.00, 'Received');

INSERT INTO inventory (
    inventory_ingredient_name,
    inventory_quantity,
    inventory_reorder_level,
    inventory_unit
)
VALUES
    ('Chicken', 25.00, 10.00, 'kg'),
    ('Basmati Rice', 30.00, 15.00, 'kg'),
    ('Beef', 9.00, 8.00, 'kg'),
    ('Naan Dough', 20.00, 15.00, 'portions'),
    ('Curry Sauce', 4.00, 5.00, 'litres'),
    ('Cooking Oil', 12.00, 8.00, 'litres');
