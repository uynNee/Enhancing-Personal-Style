import random
import pandas as pd
# /utils/content_based_filtering.py
articleType_mappings = {
    'Rectangle': ['Skirts', 'Shorts', 'Trousers', 'Track Pants', 'Capris', 'Tracksuits', 'Tshirts', 'Shirts', 'Tops',
                  'Sweatshirts', 'Jackets', 'Sweaters'],
    'Triangle': ['Jeggings', 'Skirts', 'Shorts', 'Tshirts', 'Shirts', 'Tops', 'Sweatshirts', 'Jackets', 'Sweaters'],
    'Inverted Triangle': ['Jeggings', 'Skirts', 'Shorts', 'Tshirts', 'Shirts', 'Tops', 'Sweatshirts', 'Jackets',
                          'Sweaters'],
    'Hourglass': ['Shorts', 'Trousers', 'Jeans', 'Leggings', 'Capris', 'Skirts', 'Tracksuits', 'Jeggings', 'Dresses',
                  'Jumpsuit', 'Waistcoat', 'Tshirts', 'Shirts', 'Tops', 'Sweatshirts', 'Jackets', 'Sweaters'],
    'Top Hourglass': ['Shorts', 'Trousers', 'Jeans', 'Leggings', 'Capris', 'Skirts', 'Jeggings', 'Dresses', 'Jumpsuit',
                      'Waistcoat', 'Tshirts', 'Shirts', 'Tops', 'Sweatshirts', 'Jackets', 'Sweaters'],
    'Bottom Hourglass': ['Shorts', 'Trousers', 'Jeans', 'Leggings', 'Capris', 'Skirts', 'Jeggings', 'Dresses',
                         'Jumpsuit', 'Waistcoat', 'Tshirts', 'Shirts', 'Tops', 'Sweatshirts', 'Jackets', 'Sweaters'],
    'Spoon': ['Shorts', 'Track Pants', 'Jeans', 'Leggings', 'Capris', 'Skirts', 'Tracksuits', 'Jeggings', 'Dresses',
              'Jumpsuit', 'Tshirts', 'Shirts', 'Tops', 'Sweatshirts', 'Jackets', 'Sweaters']
}

skin_mappings = {
    'Spring': ['beige', 'cream', 'gold', 'lavender', 'nude', 'off white', 'peach', 'pink', 'rose', 'kin', 'tan',
               'white', 'yellow', 'black'],
    'Summer': ['beige', 'blue', 'bronze', 'copper', 'cream', 'gold', 'green', 'khaki', 'lavender', 'nude', 'off white',
               'peach', 'pink', 'rose', 'silver', 'kin', 'tan', 'turquoise blue', 'white', 'black'],
    'Autumn': ['bronze', 'brown', 'burgundy', 'coffee brown', 'copper', 'gold', 'green', 'khaki', 'maroon',
               'mushroom brown', 'mustard', 'olive', 'orange', 'red', 'rust', 'tan', 'taupe', 'black', 'white'],
    'Winter': ['black', 'blue', 'charcoal', 'grey', 'grey melange', 'magenta', 'mauve', 'metallic', 'navy blue',
               'purple', 'red', 'silver', 'steel', 'teal', 'turquoise blue', 'white', 'black']
}


def filter_dataframe(dataframe, recommended_shape, recommended_skin, gender):
    if gender == "Unisex":
        filtered_df = dataframe[(dataframe['baseColour'].isin(recommended_skin)) &
                                (dataframe['articleType'].isin(recommended_shape)) &
                                (dataframe['gender'].isin(["Men", "Women"]))]
    else:
        filtered_df = dataframe[(dataframe['baseColour'].isin(recommended_skin)) &
                                (dataframe['articleType'].isin(recommended_shape)) &
                                (dataframe['gender'] == gender)]
    return filtered_df


def get_top_n_items(dataframe, recommended_shape, recommended_skin, gender, n=5):
    filtered_df = filter_dataframe(dataframe, recommended_shape, recommended_skin, gender)
    top_n_items = filtered_df.groupby('articleType').head(n)['id'].tolist()
    return top_n_items


def get_all_recommendations(dataframe, recommended_shape, recommended_skin, gender):
    filtered_df = filter_dataframe(dataframe, recommended_shape, recommended_skin, gender)
    all_items = filtered_df['id'].tolist()
    return all_items


def get_similar_items(knn_model, dataframe, top_n_items, recommended_shape, recommended_skin, gender, n=5):
    similar_items = top_n_items

    sparse_matrix_products = dataframe[
        ['gender', 'masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'usage',
         'productDisplayName', 'productDescription']]
    sparse_matrix_products = sparse_matrix_products[(sparse_matrix_products['baseColour'].isin(recommended_skin)) &
                                                    (sparse_matrix_products['articleType'].isin(recommended_shape)) &
                                                    (sparse_matrix_products['gender'] == gender)]
    sparse_matrix_products = sparse_matrix_products[~sparse_matrix_products.index.isin(top_n_items)]
    sparse_matrix_products = pd.get_dummies(sparse_matrix_products)
    for item_id in top_n_items:
        if item_id in sparse_matrix_products.index:
            distances, indices = knn_model.kneighbors(sparse_matrix_products.loc[item_id, :].values.reshape(1, -1))
            for i in range(n):
                similar_items.append(sparse_matrix_products.index[indices[0][i]])
    return similar_items


def select_random_cbf_products(cbf_recommendations, dataframe, n=5):
    if len(cbf_recommendations) <= n:
        selected_products = dataframe[dataframe['id'].isin(cbf_recommendations)]
    else:
        selected_product_ids = random.sample(cbf_recommendations, n)
        selected_products = dataframe[dataframe['id'].isin(selected_product_ids)]
    return selected_products


def random_recommendations(db, gender, n=5):
    query = (f"SELECT * FROM store_product WHERE gender = '{gender}'"
             f" AND subCategory IN ('Topwear', 'Bottomwear', 'Dress') ORDER BY RANDOM() LIMIT {n}")
    selected_products = pd.read_sql_query(query, db)
    return selected_products
