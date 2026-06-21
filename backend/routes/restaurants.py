from flask import Blueprint, jsonify, request
from database import get_connection

restaurants_bp = Blueprint('restaurants', __name__)

@restaurants_bp.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    search = request.args.get('search', '').lower()
    conn = get_connection()
    cursor = conn.cursor()
    if search:
        cursor.execute("SELECT * FROM restaurants WHERE LOWER(name) LIKE ? OR LOWER(cuisine) LIKE ?", (f'%{search}%', f'%{search}%'))
    else:
        cursor.execute("SELECT * FROM restaurants")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@restaurants_bp.route('/api/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurants WHERE id = ?", (restaurant_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(row))
