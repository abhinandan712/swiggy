from flask import Blueprint, jsonify
from database import get_connection
import time, threading

tracking_bp = Blueprint('tracking', __name__)

STATUSES = ['Placed', 'Confirmed', 'Preparing', 'Out for Delivery', 'Delivered']

def auto_update_status(order_id):
    for i, status in enumerate(STATUSES[1:], 1):
        time.sleep(30)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
        conn.commit()
        conn.close()

@tracking_bp.route('/api/orders/<int:order_id>/track', methods=['GET'])
def track_order(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, created_at FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    conn.close()
    if not order:
        return jsonify({"error": "Order not found"}), 404
    status = order['status']
    step = STATUSES.index(status) if status in STATUSES else 0
    return jsonify({"status": status, "step": step, "total_steps": len(STATUSES), "statuses": STATUSES})

@tracking_bp.route('/api/orders/<int:order_id>/start-tracking', methods=['POST'])
def start_tracking(order_id):
    t = threading.Thread(target=auto_update_status, args=(order_id,), daemon=True)
    t.start()
    return jsonify({"success": True})
