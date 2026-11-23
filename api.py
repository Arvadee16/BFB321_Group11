from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from pymysql.err import IntegrityError

from models import (
    create_inventory_item,
    get_inventory,
    get_inventory_item,
    update_inventory_item,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.get("/inventory")
def inventory_list():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 10))
    except ValueError:
        return jsonify({"error": "Page and size must be integers"}), 400

    if page < 1 or size < 1 or size > 100:
        return jsonify({"error": "Page must be at least 1 and size must be 1 to 100"}), 400

    name = request.args.get("name")
    items = get_inventory(page, size, name)

    return jsonify({
        "page": page,
        "size": size,
        "items": items,
    }), 200


@api_bp.get("/inventory/<int:inventory_id>")
def inventory_detail(inventory_id):
    item = get_inventory_item(inventory_id)

    if item is None:
        return jsonify({"error": "Inventory item not found"}), 404

    return jsonify(item), 200


@api_bp.post("/inventory")
@jwt_required()
def inventory_create():
    data = request.get_json(silent=True) or {}

    required = [
        "inventory_ingredient_name",
        "inventory_quantity",
        "inventory_reorder_level",
        "inventory_unit",
    ]

    if any(field not in data for field in required):
        return jsonify({"error": "All inventory fields are required"}), 400

    try:
        quantity = float(data["inventory_quantity"])
        reorder_level = float(data["inventory_reorder_level"])

        if quantity < 0 or reorder_level < 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "Quantity and reorder level must be non-negative numbers"}), 400

    try:
        item = create_inventory_item(
            data["inventory_ingredient_name"],
            quantity,
            reorder_level,
            data["inventory_unit"],
        )
    except IntegrityError:
        return jsonify({"error": "Ingredient name already exists"}), 400

    return jsonify(item), 201


@api_bp.patch("/inventory/<int:inventory_id>")
@jwt_required()
def inventory_update(inventory_id):
    if get_inventory_item(inventory_id) is None:
        return jsonify({"error": "Inventory item not found"}), 404

    data = request.get_json(silent=True) or {}

    if "inventory_quantity" not in data or "inventory_reorder_level" not in data:
        return jsonify({"error": "Quantity and reorder level are required"}), 400

    try:
        quantity = float(data["inventory_quantity"])
        reorder_level = float(data["inventory_reorder_level"])

        if quantity < 0 or reorder_level < 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "Quantity and reorder level must be non-negative numbers"}), 400

    item = update_inventory_item(inventory_id, quantity, reorder_level)
    return jsonify(item), 200