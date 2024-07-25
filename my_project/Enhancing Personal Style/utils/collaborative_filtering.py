import pandas as pd
from flask import session
from sklearn.metrics.pairwise import cosine_similarity
# /utils/collaborative_filtering.py


def collaborative_filtering(user_likes_df):
    user_item_matrix = user_likes_df.pivot_table(index='user_id', columns='item_id', aggfunc='size', fill_value=0)
    user_similarity = cosine_similarity(user_item_matrix)
    user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)
    user_id = session['user_id']
    if user_id in user_similarity_df.columns:
        similar_users = user_similarity_df[user_id].sort_values(ascending=False).index[1:]
        similar_users_likes = user_item_matrix.loc[similar_users].sum(axis=0).sort_values(ascending=False)
        liked_products = user_likes_df[user_likes_df['user_id'] == user_id]['item_id'].tolist()
        recommendations = similar_users_likes[~similar_users_likes.index.isin(liked_products)].head(5).index.tolist()
    else:
        recommendations = []
    return recommendations
