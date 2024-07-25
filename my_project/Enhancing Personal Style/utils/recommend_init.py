import pickle
from collections import OrderedDict
import pandas as pd
from utils.content_based_filtering import skin_mappings, articleType_mappings, get_top_n_items, get_similar_items
from utils.integrate_link import generate_search_urls
# utils/collaborative_filtering.py


def fetch_recommendation_data(user_id, db, request_args):
    shape, gender, skin_tone = get_user_preferences(user_id, db, request_args)
    knn_model = load_knn_model()
    recommended_shape = articleType_mappings.get(shape, [])
    recommended_skin = skin_mappings.get(skin_tone, [])
    query = "SELECT * FROM store_product"
    dataframe = pd.read_sql_query(query, db)
    top_n_items = get_top_n_items(dataframe, recommended_shape, recommended_skin, gender)
    cbf_recommendations = get_similar_items(knn_model, dataframe, top_n_items, recommended_shape, recommended_skin,
                                            gender)
    return shape, gender, skin_tone, dataframe, cbf_recommendations


def get_user_preferences(user_id, db, request_args):
    query_preferences = "SELECT body_shape, gender, skin_tone FROM user_preferences WHERE user_id = ?"
    user_preferences = db.execute(query_preferences, (user_id,)).fetchone()
    if user_preferences:
        shape = user_preferences[0]
        gender = user_preferences[1]
        skin_tone = user_preferences[2]
    else:
        shape = request_args.get('shape')
        gender = request_args.get('gender')
        skin_tone = request_args.get('skin_tone')
    return shape, gender, skin_tone


def load_knn_model(filepath='clothing_knn.pkl'):
    with open(filepath, 'rb') as f:
        knn_model = pickle.load(f)
    return knn_model


def process_recommendations(cbf_recommendations, cf_recommendations, dataframe, user_likes_df, skin_tone, gender):
    recommended_skin = skin_mappings.get(skin_tone, [])
    final_recommendations = []
    for item_id in cbf_recommendations:
        product = dataframe[dataframe['id'] == item_id]
        if not product.empty:
            product_details = extract_product_details(product)
            if product_details['base_color'] in recommended_skin:
                product_details['liked_by_count'] = user_likes_df[user_likes_df['item_id'] == item_id].shape[0]
                product_name_for_search = product_details['product_display_name'].replace(" ", "+")
                amazon_url = generate_search_urls([product_name_for_search])
                product_details.update({
                    'amazon_search_url': amazon_url,
                    'recommended_by': 'content_based_filtering'
                })
                final_recommendations.append(product_details)
    for item_id in cf_recommendations:
        product = dataframe[dataframe['id'] == item_id]
        if not product.empty:
            product_details = extract_product_details(product)
            if gender in ['Men', 'Women'] and product_details['gender'] not in [gender, 'Unisex']:
                continue
            product_details['liked_by_count'] = user_likes_df[user_likes_df['item_id'] == item_id].shape[0]
            product_name_for_search = product_details['product_display_name'].replace(" ", "+")
            amazon_url = generate_search_urls([product_name_for_search])
            product_details.update({
                'amazon_search_url': amazon_url,
                'recommended_by': 'collaborative_filtering'
            })
            final_recommendations.append(product_details)
    return final_recommendations


def group_recommendations_by_subcategory(recommendations):
    ordered_subcategories = ['Topwear', 'Bottomwear', 'Dress']
    grouped_recommendations = OrderedDict((subcategory, []) for subcategory in ordered_subcategories)
    for product in recommendations:
        subcategory = product['subCategory']
        if subcategory in grouped_recommendations:
            grouped_recommendations[subcategory].append(product)

    return {subcategory: products for subcategory, products in grouped_recommendations.items() if products}


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
