import numpy as np
import pandas as pd
from flask import g, Flask
from utils.content_based_filtering import get_all_recommendations, articleType_mappings, skin_mappings
from utils.database import get_db
# evaluate.py
app = Flask(__name__)


def fetch_user_preferences_and_relevant_items(user_Id):
    with app.app_context():
        g.db = get_db()
        db = g.db

        query = "SELECT * FROM store_product"
        dataframe = pd.read_sql_query(query, db)

        query = "SELECT body_shape, gender, skin_tone FROM user_preferences WHERE user_id = ?"
        user_preferences = db.execute(query, (user_Id,)).fetchone()
        if not user_preferences:
            return None, None, None, None, 0

        shape, gender, skin_tone = user_preferences
        recommended_shape = articleType_mappings.get(shape, [])
        recommended_skin = skin_mappings.get(skin_tone, [])
        relevant_items = get_all_recommendations(dataframe, recommended_shape, recommended_skin, gender)

        Count = len(relevant_items)

        return shape, gender, skin_tone, relevant_items, Count


def precision_at_n(user_Id, N):
    shape, gender, skin_tone, relevant_items, _ = fetch_user_preferences_and_relevant_items(user_Id)
    if not relevant_items:
        return 0

    recommended_items = relevant_items[:N]
    relevant_count = sum(1 for item in recommended_items if item in relevant_items)

    precision = relevant_count / N
    return precision


def recall_at_n(user_Id, N):
    shape, gender, skin_tone, relevant_items, _ = fetch_user_preferences_and_relevant_items(user_Id)
    if not relevant_items:
        return 0

    top_n_items = relevant_items[:N]
    relevant_count = sum(1 for item in top_n_items if item in relevant_items)

    recall = relevant_count / len(relevant_items) if relevant_items else 0
    return recall


def mean_average_precision(U, K, start):
    total_precision = 0
    user_count = 0

    for user_Id in range(start, U + start):
        shape, gender, skin_tone, relevant_items, _ = fetch_user_preferences_and_relevant_items(user_Id)
        if not relevant_items:
            continue

        recommended_items = relevant_items[:K]
        precision_at_k = [len(set(relevant_items) & set(recommended_items[:k])) / k for k in range(1, K + 1)]
        average_precision = np.mean(precision_at_k)
        total_precision += average_precision
        user_count += 1

    mean_avg_precision = total_precision / user_count if user_count > 0 else 0
    return mean_avg_precision


def dcg(relevance_scores):
    return sum((2**rel - 1) / np.log2(i + 2) for i, rel in enumerate(relevance_scores))


def idcg(relevance_scores):
    return dcg(sorted(relevance_scores, reverse=True))


def normalized_discounted_cumulative_gain(user_Id, N):
    shape, gender, skin_tone, relevant_items, _ = fetch_user_preferences_and_relevant_items(user_Id)
    if not relevant_items:
        return 0

    recommended_items = relevant_items[:N]
    relevance_scores = [1 if item in relevant_items else 0 for item in recommended_items]
    dcg_score = dcg(relevance_scores)
    idcg_score = idcg(relevance_scores)
    ndcg = dcg_score / idcg_score if idcg_score > 0 else 0
    return ndcg


if __name__ == "__main__":
    user_id = 9
    u = 10  # Number of users

    for i in range(user_id, u + user_id):
        shape, gender, skin_tone, _, count = fetch_user_preferences_and_relevant_items(i)
        n = count
        print(f"Tester {i-8}: ", shape, gender, skin_tone)
        print(f"Number of relevant items for user {i}: ", count)
        print(f"Precision at N score for user {i}: ", precision_at_n(i, n))
        print(f"Recall at N score for user {i}: ", recall_at_n(i, n))
        print(f"Normalized Discounted Cumulative Gain for user {i}: ",
              normalized_discounted_cumulative_gain(i, n), "\n\n")

    n = 1000
    print(f"__________\nMean Average Precision on {n} items: ", mean_average_precision(u, n, user_id), "\n__________")
