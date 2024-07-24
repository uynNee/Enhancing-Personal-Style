# routes/test.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf.csrf import generate_csrf

from routes.main import handle_form_request
from utils.prediction import predict_body_shape

test_bp = Blueprint('test', __name__)


@test_bp.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        shape, gender, skin_tone = handle_form_request(request.form)
        return redirect(url_for('recommendations.test_recommend', shape=shape, gender=gender, skin_tone=skin_tone))
    return render_template('user_testing.html', csrf_token=generate_csrf())
