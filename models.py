from db import execute, query_all, query_one


def get_inventory(page=1, size=10, name=None):
    offset = (page - 1) * size

    if name:
        return query_all(
            """
            SELECT inventory_id,
                   inventory_ingredient_name,
                   inventory_quantity,
                   inventory_reorder_level,
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
        SELECT inventory_id,
               inventory_ingredient_name,
               inventory_quantity,
               inventory_reorder_level,
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
        SELECT inventory_id,
               inventory_ingredient_name,
               inventory_quantity,
               inventory_reorder_level,
               inventory_unit
        FROM inventory
        WHERE inventory_id = %s
        """,
        (inventory_id,),
    )


def create_inventory_item(
    name,
    quantity,
    reorder_level,
    unit,
):
    new_id = execute(
        """
        INSERT INTO inventory
            (
                inventory_ingredient_name,
                inventory_quantity,
                inventory_reorder_level,
                inventory_unit
            )
        VALUES (%s, %s, %s, %s)
        """,
        (
            name,
            quantity,
            reorder_level,
            unit,
        ),
    )

    return get_inventory_item(new_id)


def update_inventory_item(
    inventory_id,
    quantity,
    reorder_level,
):
    execute(
        """
        UPDATE inventory
        SET inventory_quantity = %s,
            inventory_reorder_level = %s,
            inventory_updated_at =
                CURRENT_TIMESTAMP
        WHERE inventory_id = %s
        """,
        (
            quantity,
            reorder_level,
            inventory_id,
        ),
    )

    return get_inventory_item(inventory_id)


def get_menu_items():
    return query_all(
        """
        SELECT menu_items_id,
               menu_items_name,
               menu_items_price,
               menu_items_prep_time
        FROM menu_items
        WHERE menu_items_available = 1
        ORDER BY menu_items_name
        """
    )


def get_menu_item(menu_items_id):
    return query_one(
        """
        SELECT menu_items_id,
               menu_items_name,
               menu_items_price,
               menu_items_prep_time
        FROM menu_items
        WHERE menu_items_id = %s
          AND menu_items_available = 1
        """,
        (menu_items_id,),
    )


def get_orders():
    return query_all(
        """
        SELECT orders.orders_id,
               orders.orders_customer_name,
               orders.orders_channel,
               orders.orders_status,
               order_items.order_items_id,
               order_items.order_items_quantity,
               order_items.order_items_unit_price,
               order_items.order_items_status,
               menu_items.menu_items_id,
               menu_items.menu_items_name
        FROM orders
        INNER JOIN order_items
            ON orders.orders_id =
               order_items.orders_id
        INNER JOIN menu_items
            ON order_items.menu_items_id =
               menu_items.menu_items_id
        ORDER BY orders.orders_id DESC
        """
    )


def get_order(orders_id):
    return query_one(
        """
        SELECT orders.orders_id,
               orders.orders_customer_name,
               orders.orders_channel,
               orders.orders_status,
               order_items.order_items_id,
               order_items.order_items_quantity,
               order_items.order_items_unit_price,
               order_items.order_items_status,
               menu_items.menu_items_id,
               menu_items.menu_items_name
        FROM orders
        INNER JOIN order_items
            ON orders.orders_id =
               order_items.orders_id
        INNER JOIN menu_items
            ON order_items.menu_items_id =
               menu_items.menu_items_id
        WHERE orders.orders_id = %s
        """,
        (orders_id,),
    )


def create_order(
    customer_name,
    channel,
    menu_items_id,
    quantity,
):
    menu_item = get_menu_item(menu_items_id)

    if menu_item is None:
        return None

    orders_id = execute(
        """
        INSERT INTO orders
            (
                orders_customer_name,
                orders_channel,
                orders_status
            )
        VALUES (%s, %s, 'Received')
        """,
        (
            customer_name,
            channel,
        ),
    )

    execute(
        """
        INSERT INTO order_items
            (
                orders_id,
                menu_items_id,
                order_items_quantity,
                order_items_unit_price,
                order_items_status
            )
        VALUES (%s, %s, %s, %s, 'Received')
        """,
        (
            orders_id,
            menu_items_id,
            quantity,
            menu_item["menu_items_price"],
        ),
    )

    return get_order(orders_id)


def update_order_status(
    orders_id,
    status,
):
    execute(
        """
        UPDATE orders
        SET orders_status = %s,
            orders_completed_at =
                CASE
                    WHEN %s = 'Completed'
                    THEN CURRENT_TIMESTAMP
                    ELSE NULL
                END,
            orders_updated_at =
                CURRENT_TIMESTAMP
        WHERE orders_id = %s
        """,
        (
            status,
            status,
            orders_id,
        ),
    )

    execute(
        """
        UPDATE order_items
        SET order_items_status = %s,
            order_items_updated_at =
                CURRENT_TIMESTAMP
        WHERE orders_id = %s
        """,
        (
            status,
            orders_id,
        ),
    )

    return get_order(orders_id)