import pandas as pd
from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from flask_wtf.csrf import generate_csrf
from utils.prediction import predict_body_shape
from utils.database import get_db, close_db
# routes/main.py

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
        shape, gender, skin_tone = handle_form_request(request.form)
        return redirect(url_for('recommendations.recommend', shape=shape, gender=gender, skin_tone=skin_tone))
    return render_template('index.html', csrf_token=generate_csrf())


@main_bp.route('/predict_shape', methods=['POST'])
def predict_shape():
    data = request.json
    gender = data.get('gender')
    chest = data.get('chest')
    waist = data.get('waist')
    high = data.get('high')
    hip = data.get('hip')
    predicted_shape = predict_body_shape(gender, chest, waist, high, hip)
    return jsonify({'predicted_shape': predicted_shape})


def handle_form_request(request_form):
    shape = request_form.get('shape')
    gender = request_form.get('gender')
    skin_tone = request_form.get('skin_tone')
    if shape == "Predict":
        chest = float(request_form.get('Chest'))
        waist = float(request_form.get('Waist'))
        high = float(request_form.get('High'))
        hip = float(request_form.get('Hip'))
        shape = predict_body_shape(gender, chest, waist, high, hip)
    return shape, gender, skin_tone
