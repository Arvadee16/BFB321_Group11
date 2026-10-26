
# MY Diners EOQ Model
# BFB 321 - Group 11

import math


def calculate_eoq(demand, order_cost, hold_cost):
    """
    Calculate Economic Order Quantity.

    Formula: EOQ = sqrt((2 * D * S) / H)

    Inputs:
    demand = annual demand in kg
    order_cost = cost per order in Rand
    hold_cost = annual holding cost per kg in Rand

    Output:
    Optimal order quantity in kg

    Assumptions:
    Demand and costs are constant.
    No shortages or quantity discounts.
    """

    if demand <= 0 or order_cost <= 0 or hold_cost <= 0:
        raise ValueError("All inputs must be greater than zero")

    return math.sqrt((2 * demand * order_cost) / hold_cost)


def total_annual_cost(demand, order_cost, hold_cost, order_qty):
    """
    Calculate annual ordering and holding costs.

    Formula:
    Total Cost = (D / Q) * S + (Q / 2) * H

    Inputs:
    demand = annual demand in kg
    order_cost = cost per order in Rand
    hold_cost = annual holding cost per kg in Rand
    order_qty = quantity ordered in kg

    Output:
    Total annual ordering and holding cost in Rand

    Assumptions:
    Demand and costs are constant.
    Average inventory is Q / 2.
    Purchase cost is excluded.
    """

    if demand <= 0 or order_cost <= 0 or hold_cost <= 0 or order_qty <= 0:
        raise ValueError("All inputs must be greater than zero")

    ordering = (demand / order_qty) * order_cost
    holding = (order_qty / 2) * hold_cost

    return ordering + holding


# MY Diners rice inventory example

if __name__ == "__main__":

    annual_demand = 2400
    ordering_cost = 100
    holding_cost = 20

    eoq = calculate_eoq(annual_demand, ordering_cost, holding_cost)

    orders_per_year = annual_demand / eoq
    days_between_orders = 365 / orders_per_year

    cost_at_eoq = total_annual_cost(
        annual_demand, ordering_cost, holding_cost, eoq
    )

    print("MY Diners Rice Inventory")
    print("------------------------")
    print("Optimal order quantity:", round(eoq, 2), "kg")
    print("Orders per year:", round(orders_per_year, 2))
    print("Days between orders:", round(days_between_orders, 1))
    print("Total annual cost at EOQ: R", round(cost_at_eoq, 2))
