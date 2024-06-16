from flask import Flask, request, jsonify, g, render_template
import numpy as np
import pickle
import sqlite3
import pandas as pd
import os
import pandas as pd
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
            Chest = float(request.form.get('Chest'))
            Waist = float(request.form.get('Waist'))
            High = float(request.form.get('High'))
            Hip = float(request.form.get('Hip'))
            shape = predict_body_shape(gender, Chest, Waist, High, Hip)
        return redirect(url_for('recommend', shape=shape, gender=gender, skin_tone=skin_tone))
    return render_template('index.html')

def predict_body_shape(gender, Chest, Waist, High, Hip):
    with open('bodyshape_model.pkl', 'rb') as file:
        pickle_model = pickle.load(file)
    gender_value = 0 if gender == 'Men' else 1
    new_data = np.array([[gender_value, Chest, Waist, High, Hip]])
    waist_hip_ratio = Waist / Hip
    new_data = np.append(new_data, [[waist_hip_ratio]], axis=1)
    predicted_shape = pickle_model.predict(new_data)[0]
    print(predicted_shape)
    predicted_shape = predicted_shape.strip('[]').strip("''")
    return predicted_shape

articleType_mappings = {
    'Rectangle': ['Skirts','Shorts', 'Trousers', 'Track Pants', 'Capris', 'Tracksuits', 'Tshirts', 'Shirts', 'Tops', 'Sweatshirts', 'Jackets', 'Sweaters'],
    'Triangle': ['Jeggings', 'Skirts','Shorts','Tshirts', 'Shirts', 'Tops', 'Sweatshirts', 'Jackets', 'Sweaters'],
    'Inverted Triangle': ['Jeggings', 'Skirts','Shorts','Tshirts', 'Shirts', 'Tops', 'Sweatshirts', 'Jackets', 'Sweaters'],
    'Hourglass': ['Shorts', 'Trousers', 'Jeans', 'Leggings', 'Capris', 'Skirts', 'Tracksuits', 'Jeggings', 'Dresses', 'Jumpsuit', 'Waistcoat', 'Tshirts', 'Shirts', 'Tops', 'Sweatshirts', 'Jackets', 'Sweaters'],
    'Top Hourglass': ['Shorts','Trousers', 'Jeans', 'Leggings', 'Capris', 'Skirts', 'Jeggings', 'Dresses', 'Jumpsuit', 'Waistcoat', 'Tshirts', 'Shirts', 'Tops', 'Sweatshirts', 'Jackets', 'Sweaters'],
    'Bottom Hourglass': ['Shorts','Trousers', 'Jeans', 'Leggings', 'Capris', 'Skirts', 'Jeggings', 'Dresses', 'Jumpsuit', 'Waistcoat', 'Tshirts', 'Shirts', 'Tops', 'Sweatshirts', 'Jackets', 'Sweaters'],
    'Spoon': ['Shorts', 'Track Pants', 'Jeans', 'Leggings', 'Capris', 'Skirts', 'Tracksuits', 'Jeggings', 'Dresses', 'Jumpsuit', 'Tshirts', 'Shirts', 'Tops', 'Sweatshirts', 'Jackets', 'Sweaters']
}

skin_mappings = {
    'Spring': ['beige', 'cream', 'gold', 'lavender', 'nude', 'off white', 'peach', 'pink', 'rose', 'kin', 'tan', 'white', 'yellow', 'black'],
    'Summer': ['beige', 'blue', 'bronze', 'copper', 'cream', 'gold', 'green', 'khaki', 'lavender', 'nude', 'off white', 'peach', 'pink', 'rose', 'silver', 'kin', 'tan', 'turquoise blue', 'white', 'black'],
    'Autumn': ['bronze', 'brown', 'burgundy', 'coffee brown', 'copper', 'gold', 'green', 'khaki', 'maroon', 'mushroom brown', 'mustard', 'olive', 'orange', 'red', 'rust', 'tan', 'taupe', 'black', 'white'],
    'Winter': ['black', 'blue', 'charcoal', 'grey', 'grey melange', 'magenta', 'mauve', 'metallic', 'navy blue', 'purple', 'red', 'silver', 'steel', 'teal', 'turquoise blue', 'white', 'black']
}

def get_top_n_items(dataframe, categories, gender, n=5):
    top_n_items = []
    for category in categories:
        filtered_df = dataframe[(dataframe['articleType'] == category) & (dataframe['gender'] == gender)]
        top_items = filtered_df.head(n)['id'].tolist()
        top_n_items.extend(top_items)
    return top_n_items

def get_similar_items(dataframe, knn_model, train_columns, items, gender, n=5):
    similar_items = set()
    dataframe_encoded = pd.get_dummies(dataframe[['masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'usage']])
    for item_id in items:
        product = dataframe[(dataframe['id'] == item_id) & (dataframe['gender'] == gender)]
        features = product[['masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'usage']]
        features_encoded = pd.get_dummies(features).reindex(columns=train_columns, fill_value=0)
        distances, indices = knn_model.kneighbors(features_encoded.values.reshape(1, -1))
        similar_items.update([dataframe.iloc[idx]['id'] for idx in indices.flatten()[1:n+1] if dataframe.iloc[idx]['gender'] == gender])  # Use update method for sets
    return list(similar_items)

@app.route('/recommend', methods=['GET'])
def recommend():
    shape = request.args.get('shape')
    gender = request.args.get('gender')
    skin_tone = request.args.get('skin_tone')
    recommended_types = articleType_mappings.get(shape, [])
    query = "SELECT * FROM store_product"
    dataframe_store_product = pd.read_sql_query(query, g.db)
    with open('clothing_knn.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
    top_n_items = get_top_n_items(dataframe_store_product, recommended_types, gender)
    dataframe_encoded = pd.get_dummies(dataframe_store_product[['masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'usage']])
    train_columns = dataframe_encoded.columns
    similar_items = get_similar_items(dataframe_store_product, loaded_model, train_columns, top_n_items, gender)
    recommended_colors = skin_mappings.get(skin_tone, [])
    final_recommendations = []
    for item_id in similar_items:
        product = dataframe_store_product[dataframe_store_product['id'] == item_id]
        product_display_name = product['productDisplayName'].values[0]
        product_image_link = product['link'].values[0]
        product_subcategory = product['subCategory'].values[0]
        product_base_color = product['baseColour'].values[0]
        if product_base_color in recommended_colors:
            final_recommendations.append({
    'product_display_name': product_display_name,
    'product_image_link': product_image_link,
    'subCategory': product_subcategory
            })
    grouped_recommendations = {}
    for product in final_recommendations:
        subcategory = product['subCategory']
        if subcategory not in grouped_recommendations:
            grouped_recommendations[subcategory] = []
        grouped_recommendations[subcategory].append(product)
    return render_template('recommendation.html', products=grouped_recommendations, user_shape=shape, user_gender=gender, user_skin_tone=skin_tone)

if __name__ == '__main__':
    app.run(debug=True)