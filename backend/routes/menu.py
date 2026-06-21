from flask import Blueprint, jsonify
from database import get_connection

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/api/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def get_menu(restaurant_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu_items WHERE restaurant_id = ?", (restaurant_id,))
    rows = cursor.fetchall()
    conn.close()
    items = [dict(row) for row in rows]
    # Group by category
    categories = {}
    for item in items:
        cat = item['category']
        categories.setdefault(cat, []).append(item)
    return jsonify({"items": items, "categories": categories})
