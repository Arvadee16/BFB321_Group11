from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from pymysql.err import IntegrityError

from models import (
    create_inventory_item,
    create_order,
    get_inventory,
    get_inventory_item,
    get_menu_item,
    get_menu_items,
    get_order,
    get_orders,
    update_inventory_item,
    update_order_status,
)

from supply_chain import (
    calculate_eoq,
    total_annual_cost,
)


api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api",
)


@api_bp.get("/inventory")
def inventory_list():
    try:
        page = int(
            request.args.get("page", 1)
        )

        size = int(
            request.args.get("size", 10)
        )
    except ValueError:
        return jsonify({
            "error":
                "Page and size must be integers"
        }), 400

    if (
        page < 1
        or size < 1
        or size > 100
    ):
        return jsonify({
            "error":
                "Page must be at least 1 "
                "and size must be 1 to 100"
        }), 400

    name = request.args.get("name")

    items = get_inventory(
        page,
        size,
        name,
    )

    return jsonify({
        "page": page,
        "size": size,
        "items": items,
    }), 200


@api_bp.get(
    "/inventory/<int:inventory_id>"
)
def inventory_detail(inventory_id):
    item = get_inventory_item(
        inventory_id
    )

    if item is None:
        return jsonify({
            "error":
                "Inventory item not found"
        }), 404

    return jsonify(item), 200


@api_bp.post("/inventory")
@jwt_required()
def inventory_create():
    data = (
        request.get_json(silent=True)
        or {}
    )

    required = [
        "inventory_ingredient_name",
        "inventory_quantity",
        "inventory_reorder_level",
        "inventory_unit",
    ]

    if any(
        field not in data
        for field in required
    ):
        return jsonify({
            "error":
                "All inventory fields "
                "are required"
        }), 400

    name = str(
        data["inventory_ingredient_name"]
    ).strip()

    unit = str(
        data["inventory_unit"]
    ).strip()

    if not name or not unit:
        return jsonify({
            "error":
                "Ingredient name and unit "
                "are required"
        }), 400

    try:
        quantity = float(
            data["inventory_quantity"]
        )

        reorder_level = float(
            data[
                "inventory_reorder_level"
            ]
        )

        if (
            quantity < 0
            or reorder_level < 0
        ):
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({
            "error":
                "Quantity and reorder level "
                "must be non-negative numbers"
        }), 400

    try:
        item = create_inventory_item(
            name,
            quantity,
            reorder_level,
            unit,
        )
    except IntegrityError:
        return jsonify({
            "error":
                "Ingredient name already exists"
        }), 400

    return jsonify(item), 201


@api_bp.patch(
    "/inventory/<int:inventory_id>"
)
@jwt_required()
def inventory_update(inventory_id):
    if (
        get_inventory_item(inventory_id)
        is None
    ):
        return jsonify({
            "error":
                "Inventory item not found"
        }), 404

    data = (
        request.get_json(silent=True)
        or {}
    )

    if (
        "inventory_quantity"
        not in data
        or "inventory_reorder_level"
        not in data
    ):
        return jsonify({
            "error":
                "Quantity and reorder level "
                "are required"
        }), 400

    try:
        quantity = float(
            data["inventory_quantity"]
        )

        reorder_level = float(
            data[
                "inventory_reorder_level"
            ]
        )

        if (
            quantity < 0
            or reorder_level < 0
        ):
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({
            "error":
                "Quantity and reorder level "
                "must be non-negative numbers"
        }), 400

    item = update_inventory_item(
        inventory_id,
        quantity,
        reorder_level,
    )

    return jsonify(item), 200


@api_bp.get("/menu-items")
def menu_items_list():
    return jsonify(
        get_menu_items()
    ), 200


@api_bp.get("/orders")
def orders_list():
    return jsonify(
        get_orders()
    ), 200


@api_bp.get("/orders/<int:orders_id>")
def order_detail(orders_id):
    order = get_order(orders_id)

    if order is None:
        return jsonify({
            "error": "Order not found"
        }), 404

    return jsonify(order), 200


@api_bp.post("/orders")
def order_create():
    data = (
        request.get_json(silent=True)
        or {}
    )

    required = [
        "orders_customer_name",
        "orders_channel",
        "menu_items_id",
        "order_items_quantity",
    ]

    if any(
        field not in data
        for field in required
    ):
        return jsonify({
            "error":
                "All order fields are required"
        }), 400

    customer_name = str(
        data["orders_customer_name"]
    ).strip()

    channel = str(
        data["orders_channel"]
    ).strip()

    if not customer_name or not channel:
        return jsonify({
            "error":
                "Customer name and channel "
                "are required"
        }), 400

    try:
        menu_items_id = int(
            data["menu_items_id"]
        )

        quantity = int(
            data["order_items_quantity"]
        )

        if (
            menu_items_id < 1
            or quantity < 1
        ):
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({
            "error":
                "Menu item and quantity "
                "must be valid"
        }), 400

    if (
        get_menu_item(menu_items_id)
        is None
    ):
        return jsonify({
            "error": "Menu item not found"
        }), 404

    try:
        order = create_order(
            customer_name,
            channel,
            menu_items_id,
            quantity,
        )
    except IntegrityError:
        return jsonify({
            "error":
                "Unable to create order"
        }), 400

    return jsonify(order), 201


@api_bp.patch(
    "/orders/<int:orders_id>"
)
def order_update(orders_id):
    if get_order(orders_id) is None:
        return jsonify({
            "error": "Order not found"
        }), 404

    data = (
        request.get_json(silent=True)
        or {}
    )

    status = str(
        data.get("orders_status", "")
    ).strip()

    valid_statuses = [
        "Received",
        "Preparing",
        "Ready",
        "Completed",
        "Cancelled",
    ]

    if status not in valid_statuses:
        return jsonify({
            "error": "Invalid order status"
        }), 400

    order = update_order_status(
        orders_id,
        status,
    )

    return jsonify(order), 200


@api_bp.post("/eoq")
def eoq_calculation():
    data = (
        request.get_json(silent=True)
        or {}
    )

    required = [
        "demand",
        "order_cost",
        "hold_cost",
    ]

    if any(
        field not in data
        for field in required
    ):
        return jsonify({
            "error":
                "Demand, order cost and "
                "holding cost are required"
        }), 400

    try:
        demand = float(data["demand"])
        order_cost = float(
            data["order_cost"]
        )
        hold_cost = float(
            data["hold_cost"]
        )

        eoq = calculate_eoq(
            demand,
            order_cost,
            hold_cost,
        )

        annual_cost = total_annual_cost(
            demand,
            order_cost,
            hold_cost,
            eoq,
        )

        orders_per_year = demand / eoq

        days_between_orders = (
            365 / orders_per_year
        )
    except (TypeError, ValueError):
        return jsonify({
            "error":
                "All EOQ inputs must be "
                "numbers greater than zero"
        }), 400

    return jsonify({
        "eoq": round(eoq, 2),
        "orders_per_year":
            round(orders_per_year, 2),
        "days_between_orders":
            round(days_between_orders, 1),
        "total_annual_cost":
            round(annual_cost, 2),
    }), 200