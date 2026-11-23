from db import execute, query_all, query_one


def get_inventory(page=1, size=10, name=None):
    offset = (page - 1) * size

    if name:
        return query_all(
            """
            SELECT inventory_id, inventory_ingredient_name,
                   inventory_quantity, inventory_reorder_level,
                   inventory_unit
            FROM inventory
            WHERE inventory_ingredient_name LIKE %s
            ORDER BY inventory_id
            LIMIT %s OFFSET %s
            """,
            (f"%{name}%", size, offset),
        )

    return query_all(
        """
        SELECT inventory_id, inventory_ingredient_name,
               inventory_quantity, inventory_reorder_level,
               inventory_unit
        FROM inventory
        ORDER BY inventory_id
        LIMIT %s OFFSET %s
        """,
        (size, offset),
    )


def get_inventory_item(inventory_id):
    return query_one(
        """
        SELECT inventory_id, inventory_ingredient_name,
               inventory_quantity, inventory_reorder_level,
               inventory_unit
        FROM inventory
        WHERE inventory_id = %s
        """,
        (inventory_id,),
    )


def create_inventory_item(name, quantity, reorder_level, unit):
    new_id = execute(
        """
        INSERT INTO inventory
            (inventory_ingredient_name, inventory_quantity,
             inventory_reorder_level, inventory_unit)
        VALUES (%s, %s, %s, %s)
        """,
        (name, quantity, reorder_level, unit),
    )
    return get_inventory_item(new_id)


def update_inventory_item(inventory_id, quantity, reorder_level):
    execute(
        """
        UPDATE inventory
        SET inventory_quantity = %s,
            inventory_reorder_level = %s,
            inventory_updated_at = CURRENT_TIMESTAMP
        WHERE inventory_id = %s
        """,
        (quantity, reorder_level, inventory_id),
    )
    return get_inventory_item(inventory_id)