from flask import Blueprint, jsonify, request
from database import get_connection

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/api/restaurants/<int:restaurant_id>/reviews', methods=['GET'])
def get_reviews(restaurant_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews WHERE restaurant_id = ? ORDER BY created_at DESC", (restaurant_id,))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@reviews_bp.route('/api/restaurants/<int:restaurant_id>/reviews', methods=['POST'])
def add_review(restaurant_id):
    data = request.get_json()
    user_name = data.get('user_name', 'Anonymous')
    rating = data.get('rating', 5)
    comment = data.get('comment', '')
    if not comment:
        return jsonify({"error": "Comment is required"}), 400
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (restaurant_id, user_name, rating, comment) VALUES (?, ?, ?, ?)",
                   (restaurant_id, user_name, rating, comment))
    # Update restaurant avg rating
    cursor.execute("SELECT AVG(rating) as avg FROM reviews WHERE restaurant_id = ?", (restaurant_id,))
    avg = round(cursor.fetchone()['avg'], 1)
    cursor.execute("UPDATE restaurants SET rating = ? WHERE id = ?", (avg, restaurant_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "new_rating": avg})
