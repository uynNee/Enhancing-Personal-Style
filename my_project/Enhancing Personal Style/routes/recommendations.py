import pandas as pd
from flask import Blueprint, render_template, request, g, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields.simple import HiddenField, SubmitField
from wtforms.validators import DataRequired
from utils.collaborative_filtering import collaborative_filtering
from utils.content_based_filtering import select_random_cbf_products, random_recommendations
from utils.recommend_init import process_recommendations, group_recommendations_by_subcategory, \
    fetch_recommendation_data
# /routes/recommendations.py
recommendations_bp = Blueprint('recommendations', __name__)


class LikeForm(FlaskForm):
    product_id = HiddenField('Product ID', validators=[DataRequired()])
    submit = SubmitField('Submit')


@recommendations_bp.route('/recommend', methods=['GET'])
def recommend():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    user_id = session.get('user_id')
    db = g.db
    shape, gender, skin_tone, dataframe, cbf_recommendations = fetch_recommendation_data(user_id, db, request.args)
    user_likes_query = "SELECT item_id FROM user_likes WHERE user_id = ?"
    user_likes = db.execute(user_likes_query, (user_id,)).fetchall()
    liked_products = [item[0] for item in user_likes]
    user_likes_query_all = "SELECT user_id, item_id FROM user_likes"
    user_likes_all = db.execute(user_likes_query_all).fetchall()
    user_likes_df = pd.DataFrame(user_likes_all, columns=['user_id', 'item_id'])
    cf_recommendations = collaborative_filtering(user_likes_df)
    final_recommendations = process_recommendations(cbf_recommendations, cf_recommendations, dataframe, user_likes_df,
                                                    skin_tone, gender)
    grouped_recommendations = group_recommendations_by_subcategory(final_recommendations)
    form = LikeForm()
    return render_template('recommendation.html', products=grouped_recommendations, user_shape=shape,
                           user_gender=gender, user_skin_tone=skin_tone, liked_products=liked_products, form=form)


@recommendations_bp.route('/test_recommend', methods=['GET'])
def test_recommend():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
    user_id = session.get('user_id')
    db = g.db
    shape, gender, skin_tone, dataframe, cbf_recommendations = fetch_recommendation_data(user_id, db, request.args)
    cbf_df = select_random_cbf_products(cbf_recommendations, dataframe)
    cbf_df['filtering'] = 'content-based'
    random_df = random_recommendations(db, gender)
    random_df['filtering'] = 'random'
    test_recommendations = pd.concat([cbf_df, random_df])
    test_recommendations = test_recommendations.sample(frac=1)
    test_recommendations_json = test_recommendations.to_json(orient='records')
    return render_template('user_testing_recommendation.html', products=test_recommendations_json,
                           user_shape=shape, user_gender=gender, user_skin_tone=skin_tone, user_id=user_id)
