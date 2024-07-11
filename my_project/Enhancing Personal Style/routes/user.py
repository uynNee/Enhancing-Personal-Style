from flask import Blueprint, render_template, request, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from utils.database import get_db

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='scrypt')

        query = "INSERT INTO user (username, password) VALUES (?, ?)"
        g.db.execute(query, (username, hashed_password))
        g.db.commit()

        return redirect(url_for('user.login'))

    return render_template('register.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = "SELECT * FROM user WHERE username = ?"
        user = g.db.execute(query, (username,)).fetchone()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('main.index'))

    return render_template('login.html')


@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('main.index'))


@user_bp.route('/like_product', methods=['POST'])
def like_product():
    product_id = request.form.get('product_id')
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('user.login'))

    query = "INSERT INTO user_likes (user_id, item_id) VALUES (?, ?)"
    g.db.execute(query, (user_id, product_id))
    g.db.commit()

    return redirect(request.referrer)
