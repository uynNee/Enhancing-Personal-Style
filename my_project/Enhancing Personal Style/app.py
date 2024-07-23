from flask import Flask
from routes.main import main_bp
from routes.user import user_bp
from routes.recommendations import recommendations_bp
from flask_wtf.csrf import CSRFProtect


# app.py
app = Flask(__name__)
app.secret_key = 'DoMaiUyenNhiBCU'
app.config['SECRET_KEY'] = 'DoMaiUyenNhiBCU'
csrf = CSRFProtect(app)
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)
app.register_blueprint(recommendations_bp)

if __name__ == '__main__':
    app.run(debug=True)