import pickle
import sqlite3
import numpy as np
import pandas as pd
from flask import Flask, request, g, render_template
from flask import redirect
from flask import url_for

app = Flask(__name__)


@app.before_request
def before_request():
    g.db = sqlite3.connect('clothing_db.sqlite3')


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/view_database', methods=['GET'])
def view_database():
    query = "SELECT * FROM store_product"
    dataframe_store_product = pd.read_sql_query(query, g.db)
    json_data = dataframe_store_product.to_json(orient='records')
    return json_data


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        shape = request.form.get('shape')
        gender = request.form.get('gender')
        skin_tone = request.form.get('skin_tone')
        if shape == "Predict":
            chest = float(request.form.get('Chest'))
            waist = float(request.form.get('Waist'))
            high = float(request.form.get('High'))
            hip = float(request.form.get('Hip'))
            shape = predict_body_shape(gender, chest, waist, high, hip)
        return redirect(url_for('recommend', shape=shape, gender=gender, skin_tone=skin_tone))
    return render_template('index.html')


def predict_body_shape(gender, chest, waist, high, hip):
    with open('bodyshape_model.pkl', 'rb') as file:
        pickle_model = pickle.load(file)
    gender_value = 0 if gender == 'Men' else 1
    new_data = np.array([[gender_value, chest, waist, high, hip]])
    waist_hip_ratio = waist / hip
    new_data = np.append(new_data, [waist_hip_ratio], axis=1)
    predicted_shape = pickle_model.predict(new_data)[0]
    print(predicted_shape)
    predicted_shape = predicted_shape.strip('[]').strip("''")
    return predicted_shape


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


def get_top_n_items(dataframe, recommended_shape, recommended_skin, gender, n=5):
    filtered_df = dataframe[(dataframe['baseColour'].isin(recommended_skin)) &
                            (dataframe['articleType'].isin(recommended_shape)) &
                            (dataframe['gender'] == gender)]
    top_n_items = filtered_df.groupby('articleType').head(n)['id'].tolist()
    return top_n_items


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


@app.route('/recommend', methods=['GET'])
def recommend():
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

    final_recommendations = []
    for item_id in similar_items:
        product = dataframe[dataframe['id'] == item_id]
        product_display_name = product['productDisplayName'].values[0]
        product_image_link = product['link'].values[0]
        product_subcategory = product['subCategory'].values[0]
        product_base_color = product['baseColour'].values[0]
        if product_base_color in recommended_skin:
            final_recommendations.append({'product_display_name': product_display_name,
                                          'product_image_link': product_image_link,
                                          'subCategory': product_subcategory})
    grouped_recommendations = {}
    for product in final_recommendations:
        subcategory = product['subCategory']
        if subcategory not in grouped_recommendations:
            grouped_recommendations[subcategory] = []
        grouped_recommendations[subcategory].append(product)

    return render_template('recommendation.html', products=grouped_recommendations, user_shape=shape,
                           user_gender=gender, user_skin_tone=skin_tone)


if __name__ == '__main__':
    app.run(debug=True)
