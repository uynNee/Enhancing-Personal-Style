# create_app.py
from flask import Flask
from routes.main import main_bp
from routes.test import test_bp
from routes.user import user_bp
from routes.recommendations import recommendations_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = 'DoMaiUyenNhiBCU'
    app.config['SECRET_KEY'] = 'DoMaiUyenNhiBCU'

    app.register_blueprint(main_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(recommendations_bp)

    return app
