
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
