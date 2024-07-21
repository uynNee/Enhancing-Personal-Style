from flask import Blueprint, render_template, request, redirect, url_for, session, g, jsonify
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# /routes/user.py
user_bp = Blueprint('user', __name__)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password, method='scrypt')

        query = "INSERT INTO user (username, password) VALUES (?, ?)"
        g.db.execute(query, (username, hashed_password))
        g.db.commit()

        return redirect(url_for('user.login'))

    return render_template('register.html', form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        query = "SELECT * FROM user WHERE username = ?"
        user = g.db.execute(query, (username,)).fetchone()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('main.index'))

    return render_template('login.html', form=form)


@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('main.index'))


@user_bp.route('/like_product', methods=['POST'])
def like_product():
    data = request.get_json()
    product_id = data.get('product_id')
    liked = data.get('liked')
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'success': False, 'message': 'User not logged in'})

    query_check = "SELECT * FROM user_likes WHERE user_id = ? AND item_id = ?"
    existing_like = g.db.execute(query_check, (user_id, product_id)).fetchone()

    if liked and not existing_like:
        query_insert = "INSERT INTO user_likes (user_id, item_id) VALUES (?, ?)"
        g.db.execute(query_insert, (user_id, product_id))
    elif not liked and existing_like:
        query_delete = "DELETE FROM user_likes WHERE user_id = ? AND item_id = ?"
        g.db.execute(query_delete, (user_id, product_id))

    g.db.commit()
    return jsonify({'success': True})


@user_bp.route('/save_preferences', methods=['POST'])
def save_preferences():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('user.login'))

    body_shape = request.form.get('shape')
    gender = request.form.get('gender')
    skin_tone = request.form.get('skin_tone')
    chest = request.form.get('Chest')
    waist = request.form.get('Waist')
    high_hip = request.form.get('High')
    hip = request.form.get('Hip')

    query_check = "SELECT * FROM user_preferences WHERE user_id = ?"
    existing_preferences = g.db.execute(query_check, (user_id,)).fetchone()

    if existing_preferences:
        query_update = """
        UPDATE user_preferences
        SET body_shape = ?, gender = ?, skin_tone = ?, chest = ?, waist = ?, high_hip = ?, hip = ?
        WHERE user_id = ?
        """
        g.db.execute(query_update, (body_shape, gender, skin_tone, chest, waist, high_hip, hip, user_id))
    else:
        query_insert = """
        INSERT INTO user_preferences (user_id, body_shape, gender, skin_tone, chest, waist, high_hip, hip)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        g.db.execute(query_insert, (user_id, body_shape, gender, skin_tone, chest, waist, high_hip, hip))

    g.db.commit()
    return redirect(url_for('recommendations.recommend'))
