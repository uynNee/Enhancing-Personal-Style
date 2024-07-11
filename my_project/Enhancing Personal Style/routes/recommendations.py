import pickle

import pandas as pd
from flask import Blueprint, render_template, request, g, session, redirect, url_for
from utils.recommendations import get_top_n_items, get_similar_items, articleType_mappings, skin_mappings
from utils.collaborative_filtering import collaborative_filtering
from utils.intergrate_link import generate_search_urls

recommendations_bp = Blueprint('recommendations', __name__)


@recommendations_bp.route('/recommend', methods=['GET'])
def recommend():
    if 'user_id' not in session:
        return redirect(url_for('user.login'))
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
    similar_items = get_similar_items(knn_model, dataframe, top_n_items, recommended_shape, recommended_skin, gender)

    # Retrieve user likes from the database
    user_likes_query = "SELECT user_id, item_id FROM user_likes"
    user_likes = g.db.execute(user_likes_query).fetchall()
    user_likes_df = pd.DataFrame(user_likes, columns=['user_id', 'item_id'])

    # Apply collaborative filtering
    cf_recommendations = collaborative_filtering(user_likes_df)

    final_recommendations = []
    for item_id in similar_items + cf_recommendations:
        product = dataframe[dataframe['id'] == item_id]
        if not product.empty:
            product_display_name = product['productDisplayName'].values[0]
            product_image_link = product['link'].values[0]
            product_subcategory = product['subCategory'].values[0]
            product_gender = product['gender'].values[0]
            product_article_type = product['articleType'].values[0]
            product_base_color = product['baseColour'].values[0]
            product_season = product['season'].values[0]
            product_usage = product['usage'].values[0]
            if product_base_color in recommended_skin:
                # Generate search URLs
                keywords = [product_gender, product_article_type, product_base_color, product_season, product_usage]
                amazon_url = generate_search_urls(keywords)
                final_recommendations.append({
                    'id': item_id,
                    'product_display_name': product_display_name,
                    'product_image_link': product_image_link,
                    'subCategory': product_subcategory,
                    'amazon_search_url': amazon_url,
                })
    grouped_recommendations = {}
    for product in final_recommendations:
        subcategory = product['subCategory']
        if subcategory not in grouped_recommendations:
            grouped_recommendations[subcategory] = []
        grouped_recommendations[subcategory].append(product)

    return render_template('recommendation.html', products=grouped_recommendations, user_shape=shape,
                           user_gender=gender, user_skin_tone=skin_tone)
