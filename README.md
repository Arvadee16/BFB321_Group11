
# MY Diners Smart Order Fulfilment System
1. Abdur-Rahmaan Vadee - u24780848
2. Ahmed Salman Bholat - u24630145
3. Kiran Allopi - u23569862
BFB 321 - Group 11

## Project Overview

The aim of the project is to provided MY Diners with an order fullfillment and supply chain mangement systrem.


The frontend solution includes the  customer order page, kitchen order page and manager dashboard page.


The supply chain model uses Python to calculate
Economic Order Quantity (EOQ).

## Step 2: Supply Chain Model

The Python model is stored in supply_chain.py. UIt is not yet connected to Flask. The model example focusses on rice inventory.


## EOQ Inputs

Annual demand (D) = 2400 kg

Ordering cost (S) = R100 per order

Annual holding cost (H) = R20 per kg

These are assumed values for demonstration purposes.

## EOQ Formula

EOQ = sqrt((2 * D * S) / H)

EOQ = sqrt((2 * 2400 * 100) / 20)

EOQ = 154.92 kg

## Additional Calculations

Number of orders per year:

Orders per year = Annual demand / EOQ

Orders per year = 2400 / 154.92

Orders per year = 15.49

Days between orders:

Days = 365 / Orders per year

Days = 23.6 days

Total annual cost:

Total cost = (D / Q) * S + (Q / 2) * H

Total annual cost = R3098.39

This cost includes ordering and holding costs only.

## Model Assumptions
Assumptions that were used are as followed;
- Annual demand is constant.
- Ordering cost remains constant.
- Holding cost remains constant.
- Replenishment occurs in batches.
- Shortages and quantity discounts are excluded.
- Average inventory is half the order quantity.
- The model does not consider limited storage space.

## Unit Testing

Unit tests are stored in test_model.py.

Four tests were performed:

1. The Rice EOQ calculation
2. The Chicken EOQ calculation
3. The Rice total annual cost
4. The Number of orders per year

All four tests passed successfully.

Test output:

Ran 4 tests

OK

Installation and Setup instructions:


Download the Project

Open the GitHub repository: https://github.com/Arvadee16/BFB321_Group11

Click the green Code button.

Select Download ZIP.

Extract the downloaded folder.


## Current Project Status

Step 1: Frontend prototype completed.

Step 2: Supply chain model and unit tests completed.

The frontend is not yet connected to the Python model.
Database and backend integration will be completed
during later project stages.

## Step 3: MySQL Data Model

The MY Diners database was made in MySQL to improve order tracking, litchen workload monitoring and inventory visibility.

### Database Tables
Database tables include:
- `kitchen_stations` stores the kitchen stations and their workload limits.
- `menu_items` stores menu information as well as connects each item to a kitchen station.
- `orders` stores customer orders, order channels as well as order statuses.
- `order_items` links orders to their menu items and records quantity, price and preparation status.
- `inventory` stores ingredient quantities, units and reorder levels.

### Table Relationships
Table relationships include:
- One kitchen station prepares many menu items.
- One order  contains many order items.
- One menu item appears in many order items.
- The `order_items` table resolves the many-to-many relationship between `orders` and `menu_items`.
- Inventory is maintained separately because the current prototype monitors ingredient stock without linking individual ingredients to menu recipes.

### Normalization

The database is normalized to Third Normal Form (3NF) where practical. Each table represents one main subject, repeating data has been separated, and non-key fields depend on the primary key of their table. The `order_items` connecting table prevents menu-item information from being repeated inside the `orders` table.

### Keys, Constraints and Audit Fields

Primary keys uniquely identify each record. Foreign keys maintain the relationships between kitchen stations, menu items, orders and order items. `NOT NULL`, `UNIQUE` and `CHECK` constraints are used to protect data quality. The tables also contain `created_at` and `updated_at` audit fields.

### Performance Indexes

The following indexes support the main read patterns of the application:

- `idx_orders_status_received` supports obtaining the order queue by status and received time.
- `idx_order_items_order_status` supports obtaining the preparation statuses for a specific order.
- `idx_inventory_quantity_reorder` supports comparisons between available quantities and reorder levels.

### Migration Plan

The initial database structure is stored in `mydinersschema.sql`. It must be executed before the seed file. Future database changes will be saved as separate numbered SQL migration files so that changes can be applied in the correct order without replacing the existing database unexpectedly. Each migration will be tested on a development database before it is applied to the main project database.

### Seed Data

The `seed.sql` file contains realistic demonstration data for kitchen stations, menu items, orders, order items and inventory. The schema file must be executed first, followed by the seed file.

### Database Setup

1. Open MySQL Workbench.
2. Open and execute `mydinersschema.sql`.
3. Open and execute `seed.sql`.
4. Refresh the Schemas panel.
5. Confirm that all five tables and the demonstration records are available.

## Step 4: Flask REST API

Flask API allows us to connect to the `my_diners_db` MySQL database and returns JSON responses.

### API Endpoints

| Method | Endpoint | Purpose | Authentication |
|---|---|---|---|
| POST | `/api/auth/login` | Generate a JWT access token | No |
| GET | `/api/inventory` | List, paginate and filter inventory | No |
| GET | `/api/inventory/<inventory_id>` | Retrieve one inventory item | No |
| POST | `/api/inventory` | Create an inventory item | JWT required |
| PATCH | `/api/inventory/<inventory_id>` | Update inventory quantity and reorder level | JWT required |

### Pagination and filtering

```text
GET /api/inventory?page=1&size=10&name=Chicken