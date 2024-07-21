import pickle
import pandas as pd
from flask import Blueprint, render_template, request, g, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields.simple import HiddenField, SubmitField
from wtforms.validators import DataRequired
from utils.content_based_filtering import get_top_n_items, get_similar_items, articleType_mappings, skin_mappings
from utils.collaborative_filtering import collaborative_filtering
from utils.integrate_link import generate_search_urls

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

    # Load user preferences
    query_preferences = "SELECT body_shape, gender, skin_tone FROM user_preferences WHERE user_id = ?"
    user_preferences = g.db.execute(query_preferences, (user_id,)).fetchone()

    if user_preferences:
        shape = user_preferences[0]  # body_shape
        gender = user_preferences[1]  # gender
        skin_tone = user_preferences[2]  # skin_tone
    else:
        shape = request.args.get('shape')
        gender = request.args.get('gender')
        skin_tone = request.args.get('skin_tone')

    recommended_shape = articleType_mappings.get(shape, [])
    recommended_skin = skin_mappings.get(skin_tone, [])
    with open('clothing_knn.pkl', 'rb') as f:
        knn_model = pickle.load(f)
    query = "SELECT * FROM store_product"
    dataframe = pd.read_sql_query(query, g.db)
    top_n_items = get_top_n_items(dataframe, recommended_shape, recommended_skin, gender)
    cbf_recommendations = get_similar_items(knn_model, dataframe, top_n_items, recommended_shape, recommended_skin,
                                            gender)

    # Get likes for the current user
    user_likes_query = "SELECT item_id FROM user_likes WHERE user_id = ?"
    user_likes = g.db.execute(user_likes_query, (user_id,)).fetchall()
    liked_products = [item[0] for item in user_likes]

    user_likes_query_all = "SELECT user_id, item_id FROM user_likes"
    user_likes_all = g.db.execute(user_likes_query_all).fetchall()
    user_likes_df = pd.DataFrame(user_likes_all, columns=['user_id', 'item_id'])

    cf_recommendations = collaborative_filtering(user_likes_df)
    final_recommendations = []
    for item_id in cbf_recommendations:
        product = dataframe[dataframe['id'] == item_id]
        if not product.empty:
            product_details = extract_product_details(product)
            if product_details['base_color'] in recommended_skin:
                product_details['liked_by_count'] = user_likes_df[user_likes_df['item_id'] == item_id].shape[0]
                keywords = [product_details['gender'], product_details['article_type'], product_details['base_color'],
                            product_details['season'], product_details['usage']]
                amazon_url = generate_search_urls(keywords)
                product_details.update({
                    'amazon_search_url': amazon_url,
                    'recommended_by': 'content_based_filtering'
                })
                final_recommendations.append(product_details)
    for item_id in cf_recommendations:
        product = dataframe[dataframe['id'] == item_id]
        if not product.empty:
            product_details = extract_product_details(product)
            product_details['liked_by_count'] = user_likes_df[user_likes_df['item_id'] == item_id].shape[0]
            keywords = [product_details['gender'], product_details['article_type'], product_details['base_color'],
                        product_details['season'], product_details['usage']]
            amazon_url = generate_search_urls(keywords)
            product_details.update({
                'amazon_search_url': amazon_url,
                'recommended_by': 'collaborative_filtering'
            })
            final_recommendations.append(product_details)
    grouped_recommendations = group_recommendations_by_subcategory(final_recommendations)

    form = LikeForm()
    return render_template('recommendation.html', products=grouped_recommendations, user_shape=shape,
                           user_gender=gender, user_skin_tone=skin_tone, liked_products=liked_products, form=form)


def extract_product_details(product):
    return {
        'id': product['id'].values[0],
        'product_display_name': product['productDisplayName'].values[0],
        'product_image_link': product['link'].values[0],
        'subCategory': product['subCategory'].values[0],
        'gender': product['gender'].values[0],
        'article_type': product['articleType'].values[0],
        'base_color': product['baseColour'].values[0],
        'season': product['season'].values[0],
        'usage': product['usage'].values[0],
    }


def group_recommendations_by_subcategory(recommendations):
    grouped_recommendations = {}
    for product in recommendations:
        subcategory = product['subCategory']
        if subcategory not in grouped_recommendations:
            grouped_recommendations[subcategory] = []
        grouped_recommendations[subcategory].append(product)
    return grouped_recommendations
