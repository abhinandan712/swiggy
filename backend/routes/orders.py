from flask import Blueprint, jsonify, request
from database import get_connection

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/api/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    customer_name = data.get('customer_name')
    address = data.get('address')
    items = data.get('items', [])
    total = sum(item['price'] * item['quantity'] for item in items)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (customer_name, address, total) VALUES (?, ?, ?)", (customer_name, address, total))
    order_id = cursor.lastrowid
    for item in items:
        cursor.execute("INSERT INTO order_items (order_id, item_name, quantity, price) VALUES (?, ?, ?, ?)",
                       (order_id, item['name'], item['quantity'], item['price']))
    conn.commit()
    conn.close()
    return jsonify({"order_id": order_id, "total": total, "status": "Placed"})

@orders_bp.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    items = cursor.fetchall()
    conn.close()
    if not order:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"order": dict(order), "items": [dict(i) for i in items]})
