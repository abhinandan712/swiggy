from flask import Flask
from flask_cors import CORS
from database import init_db
from routes.restaurants import restaurants_bp
from routes.menu import menu_bp
from routes.orders import orders_bp
from routes.auth import auth_bp
from routes.reviews import reviews_bp
from routes.tracking import tracking_bp
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'swiggy_secret_key')
CORS(app, origins="*")

app.register_blueprint(restaurants_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(tracking_bp)

@app.route('/')
def home():
    return {'message': 'Swiggy Clone API is running!'}

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)

init_db()
