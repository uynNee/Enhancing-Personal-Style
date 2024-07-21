import pandas as pd
from flask import Blueprint, render_template, request, g, redirect, url_for
from flask_wtf.csrf import generate_csrf

from utils.prediction import predict_body_shape
from utils.database import get_db, close_db

# /routes/main.py
main_bp = Blueprint('main', __name__)


@main_bp.before_app_request
def before_request():
    g.db = get_db()


@main_bp.teardown_app_request
def teardown_request(exception):
    close_db()


@main_bp.route('/view_database', methods=['GET'])
def view_database():
    query = "SELECT * FROM store_product"
    dataframe_store_product = pd.read_sql_query(query, g.db)
    json_data = dataframe_store_product.to_json(orient='records')
    return json_data


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        shape = request.form.get('shape')
        gender = request.form.get('gender')
        skin_tone = request.form.get('skin_tone')
        if shape == "Predict":
            chest = float(request.form.get('Chest'))
            waist = float(request.form.get('Waist'))
            high = float(request.form.get('High'))
            hip = float(request.form.get('Hip'))
            shape = predict_body_shape(gender, chest, waist, high, hip)
        return redirect(url_for('recommendations.recommend', shape=shape, gender=gender, skin_tone=skin_tone))
    return render_template('index.html', csrf_token=generate_csrf())
