# %%
"""
# Packages import
"""

# %%
"""
## onetime installer
"""

# %%
# !pip install matplotlib
# !pip install pandas
# !pip install bs4
# !pip install numpy
# !pip install nltk
# !pip install scipy==1.12
# !pip install gensim
# !pip install seaborn
# !pip install scikit-learn
# !pip install plotly
# !pip install sqlalchemy
# nltk.download('stopwords')
# !pip install requests

# %%
"""
## import
"""

# %%
#import all the necessary packages.
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import math
import time
import re
import random
import os
import seaborn as sns
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity  
from sklearn.metrics import pairwise_distances
from matplotlib import gridspec
from scipy.sparse import hstack
from scipy.linalg import triu
import plotly
import requests
from PIL import Image

plotly.offline.init_notebook_mode(connected=True)
warnings.filterwarnings("ignore")

# %%
"""
# Data Import
"""

# %%
data = pd.read_csv(r'D:\OneDrive - Birmingham City University\Individual Honours Project\Might need for individual prj\my_project\data\fashion products small\styles-nhii.csv')
print('Number of data points : ', data.shape[0], \
      'Number of features/variables:', data.shape[1])

print(data.columns)
data.head()

# %%
"""
Dropping:
- year (unrelated to the model)
"""

# %%
data.drop(['year'], axis=1, inplace=True)
print ('Number of data points : ', data.shape[0], \
       'Number of features:', data.shape[1])
data.head()

# %%
"""
- adding image urls into the dataset
"""

# %%
add_data = pd.read_csv(r'D:\OneDrive - Birmingham City University\Individual Honours Project\Might need for individual prj\my_project\data\fashion products small\images.csv')
print(add_data.columns)

# %%
add_data['filename'] = add_data['filename'].apply(lambda x: x.split('.')[0])
add_data.rename(columns={'filename':'id'}, inplace=True)

print(add_data.columns)

# %%
# add the link column in add_data to data
data['id'] = data['id'].astype(str)
add_data['id'] = add_data['id'].astype(str)

data = pd.merge(data, add_data, on='id')

data.head()

# %%
"""
# Data pre-processing
"""

# %%
"""
### Deleting null values
"""

# %%
data = data.dropna()
print('Number of data points after dropping rows with any NULLs:', data.shape[0])

# %%
"""
### Adding new column
"""

# %%
# print all unique values of articleType in the alphabetical order
print(sorted(data['articleType'].unique()))

# %%
def join_unique_words(row):
    product_display_name_words = set(str(row['productDisplayName']).split())
    words = set()  # A set to store unique words

    # Iterate over each column
    for col in row.index:
        if col not in ['id', 'productDisplayName', 'link', 'productDescription']:
            for word in str(row[col]).split():
                if word not in product_display_name_words:
                    words.add(word)

    return ' '.join(words)

# Apply the function to each row
data['productDescription'] = data.apply(join_unique_words, axis=1)

# Concatenate 'productDisplayName' and 'productDescription'
data['productDescription'] = data[['productDisplayName','productDescription']].astype(str).agg(' '.join, axis=1)

pd.set_option('display.max_colwidth', None)
print(data['productDescription'].head())
print(data['productDisplayName'].head())

# %%
"""
### Remove products with brief description
"""

# %%
# Remove All products with very few words in title
data_sorted = data[data['productDescription'].apply(lambda x: len(x.split())>4)]
print("After removal of products with short description:", data_sorted.shape[0])

# %%
"""
### Removing products with dual titles per sort
1. The data is sorted based on the product description.
2. For each product, the code splits the product description into individual words.
3. The code then compares this product with the next one in the sorted list. If the number of differing words is more than 2, the products are considered different, and both are kept in the dataset. If the number of differing words is 2 or less, the products are considered the same, and the second product is removed from the dataset.
4. This process is repeated until all products have been compared.
"""

# %%
print('The number of entries with duplicate title is %d'%sum(data.duplicated('productDescription')))
data_sorted.sort_values('productDescription',inplace=True, ascending=False)

indices = []
for i,row in data_sorted.iterrows():
    indices.append(i)
import itertools
stage1_dedupe_asins = []
i = 0
j = 0
num_data_points = data_sorted.shape[0]
while i < num_data_points and j < num_data_points:    
    previous_i = i
    a = data['productDescription'].loc[indices[i]].split()
    j = i+1
    while j < num_data_points:
        b = data['productDescription'].loc[indices[j]].split()
        length = max(len(a), len(b))
        count  = 0
        for k in itertools.zip_longest(a,b): 
            if (k[0] == k[1]):
                count += 1
        if (length - count) > 2:
            stage1_dedupe_asins.append(data_sorted['id'].loc[indices[i]])
            if j == num_data_points-1: stage1_dedupe_asins.append(data_sorted['id'].loc[indices[j]])
            i = j
            break
        else:
            j += 1
    if previous_i == i:
        break

data = data.loc[data['id'].isin(stage1_dedupe_asins)]
print('Number of data points now is: ', data.shape[0])

# %%
"""
# Text Preprocessing
"""

# %%
# we use the list of stop words that are downloaded from nltk lib.
stop_words = set(stopwords.words('english'))
print ('list of stop words:', stop_words)

def nlp_preprocessing(total_text, index, column):
    if type(total_text) is not int:
        string = ""
        for words in total_text.split():
            # remove the special chars in review like '"#$@!%^&*()_+-~?>< etc.
            word = ("".join(e for e in words if e.isalnum()))
            # Conver all letters to lower-case
            word = word.lower()
            # stop-word removal
            if not word in stop_words:
                string += word + " "
        data[column][index] = string

# %%
import sys
np.set_printoptions(threshold=sys.maxsize)

# %%
data["baseColour"] = data["baseColour"].str.lower()

# %%
data.head()

# %%
unique = data['gender'].unique()
print(unique)
unique = data['masterCategory'].unique()
print(unique)
unique = data['subCategory'].unique()
print(unique)
unique = data['articleType'].unique()
print(unique)
unique = data['baseColour'].unique()
print(unique)

# %%
start_time = time.time()
# we take each title and we text-preprocess it.
for index, row in data.iterrows():
    nlp_preprocessing(row['productDescription'], index, 'productDescription')
# we print the time it took to preprocess whole titles 
print(time.time() - start_time, "seconds")

data.head()

# %%
data.reset_index(inplace=True)

# %%
data.drop("index",axis=1,inplace=True)

# %%
data['baseColour'] = data['baseColour'].astype(str)

# %%
def convrt_remove_dup(x):
    x =x.split(",")
    x = list(dict.fromkeys(x))
    x = ",".join(x)
    return x

# %%
data["baseColour"] = data["baseColour"].apply(lambda x: convrt_remove_dup(x))

# %%
data['baseColour'] = data['baseColour'].astype(str)

# %%
len(data["baseColour"].unique())

# %%
pd.set_option("display.max_colwidth", None)

# %%
data.index[data['id'] == '48123'].tolist()

# %%
data["link"].describe()

# %%
# drop all undefined links
data = data[data['link'] != 'undefined']
data["link"].describe()

# %%
# drop duplicate links
data = data.drop_duplicates(subset='link', keep='first')

# %%
data.describe()

# %%
data.reset_index(inplace=True)

# %%
data.drop("index",axis=1,inplace=True)
data

# %%
import os
import pandas as pd

cwd = os.getcwd()
print(cwd)
file_path = cwd + "\\clothingdata_final.csv"

data.to_csv(file_path)

# %%
df = pd.read_csv(file_path)
df

# %%
df.drop(["Unnamed: 0"],axis=1,inplace=True)
df.info()

# %%
df.reset_index(inplace=True)

# %%
df.drop('index',axis=1,inplace=True)

# %%
df.rename(columns={"level_0": "id"},inplace=True)
df

# %%
"""
DATA Connection
"""

# %%
import sqlite3
conn = sqlite3.connect('clothing_db.sqlite3')
c = conn.cursor()

# list all columns of df
print(df.columns)

# %%
c.execute('CREATE TABLE IF NOT EXISTS store_product (id integer, gender text, masterCategory text, subCategory text, articleType text, baseColour text, season text, usage text, productDisplayName text, link text, productDescription text)')

conn.commit()
df.to_sql('store_product', conn, if_exists='replace', index = False)
conn.close()
df.to_csv("clothingdata_finalx.csv")

# %%
"""
DATA EXTRACT
"""

# %%
from sqlalchemy import create_engine

cnx = create_engine('sqlite:///clothing_db.sqlite3').connect()

dataframe_store_product = pd.read_sql_table('store_product', cnx)
dataframe_store_product

# %%
# Utility Functions
# Display an image
def display_img(url,ax,fig):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    plt.imshow(img)

def plot_heatmap(keys, values, labels, url, text):
        gs = gridspec.GridSpec(2, 2, width_ratios=[4,1], height_ratios=[4,1]) 
        fig = plt.figure(figsize=(25,3))
        ax = plt.subplot(gs[0])
        ax = sns.heatmap(np.array([values]), annot=np.array([labels]))
        ax.set_xticklabels(keys)
        ax.set_title(text)
        ax = plt.subplot(gs[1])
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        display_img(url, ax, fig)
        plt.show()
    
def plot_heatmap_image(doc_id, vec1, vec2, url, text, model):
    intersection = set(vec1.keys()) & set(vec2.keys()) 
    for i in vec2:
        if i not in intersection:
            vec2[i]=0
    keys = list(vec2.keys())
    values = [vec2[x] for x in vec2.keys()]    
    if model == 'bag_of_words':
        labels = values
    elif model == 'tfidf':
        labels = []
        for x in vec2.keys():
            if x in  tfidf_title_vectorizer.vocabulary_:
                labels.append(tfidf_title_features[doc_id, tfidf_title_vectorizer.vocabulary_[x]])
            else:
                labels.append(0)
    elif model == 'idf':
        labels = []
        for x in vec2.keys():
            if x in  idf_title_vectorizer.vocabulary_:
                labels.append(idf_title_features[doc_id, idf_title_vectorizer.vocabulary_[x]])
            else:
                labels.append(0)
    plot_heatmap(keys, values, labels, url, text)

def text_to_vector(text):
    word = re.compile(r'\w+')
    words = word.findall(text)
    return Counter(words)

def get_result(doc_id, content_a, content_b, url, model):
    text1 = content_a
    text2 = content_b
    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)
    plot_heatmap_image(doc_id, vector1, vector2, url, text2, model)

# %%
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.stem.snowball import SnowballStemmer
import nltk
stemmer = SnowballStemmer("english")

# %%
def clean_tokenize(document):
    document = re.sub('[^\w_\s-]', ' ',document)       #remove punctuation marks and other symbols
    tokens = nltk.word_tokenize(document)              #Tokenize sentences
    cleaned_article = ' '.join([stemmer.stem(item) for item in tokens])    #Stemming each token
    return cleaned_article

# %%
import gensim.downloader

# %%
print(list(gensim.downloader.info()['models'].keys()))

# %%
data

# %%
"""
<h3> GLOBAL Model returing only ASIN"s </h3>
"""

# %%
idf_title_vectorizer = CountVectorizer()
idf_title_features = idf_title_vectorizer.fit_transform(data['productDescription'])

def n_containing(word):
    # return the number of documents which had the given word
    return sum(1 for blob in data['productDescription'] if word in blob.split())

def idf(word):
    # idf = log(#number of docs / #number of docs which had the given word)
    return math.log(data.shape[0] / (n_containing(word)))

idf_euclidean=[]
def idf_model(doc_id, num_results):
    M=[]
    pairwise_dist = pairwise_distances(idf_title_features,idf_title_features[doc_id])

    indices = np.argsort(pairwise_dist.flatten())[0:num_results]
    pdists  = np.sort(pairwise_dist.flatten())[0:num_results]

    df_indices = list(data.index[indices])

    for i in range(0,len(indices)):

        M.append(data['id'].loc[df_indices[i]])

    return M

tfidf_title_vectorizer = TfidfVectorizer(min_df = 0.0)
tfidf_title_features = tfidf_title_vectorizer.fit_transform(data['productDescription'])
tf_idf_euclidean=[]
def tfidf_model(doc_id, num_results):

    L=[]
    pairwise_dist = pairwise_distances(tfidf_title_features,tfidf_title_features[doc_id])

    indices = np.argsort(pairwise_dist.flatten())[0:num_results]
    pdists  = np.sort(pairwise_dist.flatten())[0:num_results]

    df_indices = list(data.index[indices])
    for i in range(0,len(indices)):
        L.append(data['id'].loc[df_indices[i]])
    return L

title_vectorizer = CountVectorizer()
title_features   = title_vectorizer.fit_transform(data['productDescription'])
title_features.get_shape()
bag_of_words_euclidean=[]
def bag_of_words_model(doc_id, num_results):

    B=[]
    pairwise_dist = pairwise_distances(title_features,title_features[doc_id])
    
    # np.argsort will return indices of the smallest distances
    indices = np.argsort(pairwise_dist.flatten())[0:num_results]
    #pdists will store the smallest distances
    pdists  = np.sort(pairwise_dist.flatten())[0:num_results]

    #data frame indices of the 9 smallest distace's
    df_indices = list(data.index[indices])
    
    for i in range(0,len(indices)):

        B.append(data['id'].loc[df_indices[i]])

    return B

def global_model(doc_id,num_results):
    G= bag_of_words_model(doc_id,num_results) + tfidf_model(doc_id,num_results) + idf_model(doc_id,num_results)
    G = list(dict.fromkeys(G))
    return G
    

# %%
"""
## 1.Bag of Words model on Product Titles and color
"""

# %%
title_vectorizer = CountVectorizer()
color_features   = title_vectorizer.fit_transform(df['baseColour'])
title_features   = title_vectorizer.fit_transform(df['productDescription'])

title_features.get_shape()
bag_of_words_euclidean=[]
def bag_of_words_model(doc_id, num_results):
    pairwise_dist = pairwise_distances(title_features,title_features[doc_id]) + pairwise_distances(color_features,color_features[doc_id])
    indices = np.argsort(pairwise_dist.flatten())[0:num_results]
    pdists  = np.sort(pairwise_dist.flatten())[0:num_results]
    df_indices = list(df.index[indices])
    for i in range(0,len(indices)):
        get_result(indices[i],df['productDescription'].loc[df_indices[0]], df['productDescription'].loc[df_indices[i]], df['link'].loc[df_indices[i]], 'bag_of_words')
        print('ID :',df['id'].loc[df_indices[i]])
        print ('Title:', df['productDescription'].loc[df_indices[i]])
        bag_of_words_euclidean.append(pdists[i])
        print ('Euclidean similarity with the query image :', pdists[i])
        print('='*60)
    print('Average euclidean distance is ',sum(bag_of_words_euclidean)/num_results)

# %%
print('Getting the similar items for document id and number of items')
bag_of_words_model(56, 6)

# %%
"""
## 2.TF-IDF BASED PRODUCT SIMILARITY
"""

# %%
tfidf_title_vectorizer = TfidfVectorizer(min_df = 0.0)
tfidf_title_features = tfidf_title_vectorizer.fit_transform(data['productDescription'])
tf_idf_euclidean=[]
def tfidf_model(doc_id, num_results):
    L=[]
    pairwise_dist = pairwise_distances(tfidf_title_features,tfidf_title_features[doc_id])

    indices = np.argsort(pairwise_dist.flatten())[0:num_results]
    pdists  = np.sort(pairwise_dist.flatten())[0:num_results]

    df_indices = list(data.index[indices])
    for i in range(0,len(indices)):
        L.append(data['id'].loc[df_indices[i]])
    return L

# %%
tfidf_title_vectorizer = TfidfVectorizer(min_df = 0.0)
tfidf_title_features = tfidf_title_vectorizer.fit_transform(data['productDescription'])
tf_idf_euclidean=[]
def tfidf_model(doc_id, num_results):
    pairwise_dist = pairwise_distances(tfidf_title_features,tfidf_title_features[doc_id])
    indices = np.argsort(pairwise_dist.flatten())[0:num_results]
    pdists  = np.sort(pairwise_dist.flatten())[0:num_results]
    df_indices = list(data.index[indices])

    for i in range(0,len(indices)):
        get_result(indices[i], data['productDescription'].loc[df_indices[0]], data['productDescription'].loc[df_indices[i]],data['link'].loc[df_indices[i]], 'tfidf')
        print('ID :',data['id'].loc[df_indices[i]])
        tf_idf_euclidean.append(pdists[i])
        print ('Eucliden distance from the given image :', pdists[i])
        print('='*125)
    print('Average euclidean distance is',sum(tf_idf_euclidean)/num_results)

# %%
"""
## 3. IDF BASED PRODUCT SIMILARITY
"""

# %%
idf_title_vectorizer = CountVectorizer()
idf_title_features = idf_title_vectorizer.fit_transform(data['productDescription'])

# %%
def n_containing(word):
    return sum(1 for blob in data['productDescription'] if word in blob.split())

def idf(word):
    return math.log(data.shape[0] / (n_containing(word)))

# %%
idf_euclidean=[]
def idf_model(doc_id, num_results):
    pairwise_dist = pairwise_distances(idf_title_features,idf_title_features[doc_id])
    indices = np.argsort(pairwise_dist.flatten())[0:num_results]
    pdists  = np.sort(pairwise_dist.flatten())[0:num_results]
    df_indices = list(data.index[indices])

    for i in range(0,len(indices)):
        get_result(indices[i],data['productDescription'].loc[df_indices[0]], data['productDescription'].loc[df_indices[i]], data['link'].loc[df_indices[i]], 'idf')
        print('ID :',data['id'].loc[df_indices[i]])
        idf_euclidean.append(pdists[i])
        print ('euclidean distance from the given image :', pdists[i])
        print('='*125)
    print('Average euclidean distance is ',sum(idf_euclidean)/num_results)

# %%
idf_model(0,5)

# %%
"""
## 4. KNN BASED PRODUCT SIMILARITY
"""

# %%
import numpy as np
import pandas as pd 
from sklearn.neighbors import NearestNeighbors

# %%
df.columns

# %%
sparse_matrix_products = df[['masterCategory', 'subCategory', 'articleType', 'baseColour', 'season', 'usage']]

# %%
sparse_matrix_products.info()

# %%
sparse_matrix_products = pd.get_dummies(sparse_matrix_products)

# %%
model = NearestNeighbors(n_neighbors=15,
                         metric='cosine',
                         algorithm='brute',
                         n_jobs=-1)
model.fit(sparse_matrix_products)

# %%
import pickle

# Assuming 'model' is your KNN model
with open('clothing_knn.pkl', 'wb') as f:
    pickle.dump(model, f)

# %%
# load the model from disk
with open('clothing_knn.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

query_index = 0  # Replace 0 with the desired index value
distances, indices = loaded_model.kneighbors(sparse_matrix_products.iloc[query_index, :].values.reshape(1, -1))

query_index = 58

distances, indices = loaded_model.kneighbors(sparse_matrix_products.iloc[query_index, :].values.reshape(1, -1))

print(len(distances.flatten()))
M=[]
D=[]
for i in range(0,10):
    if i==0:
        print("Recommendation for {0}:\n".format(sparse_matrix_products.index[query_index]))
    else:
        M.append(sparse_matrix_products.index[indices.flatten()[i]])
        D.append(distances.flatten()[i])
        print("{0}: {1}, with distance of {2}".format(i,sparse_matrix_products.index[indices.flatten()[i]],distances.flatten()[i]))

# %%
for i in range(0,len(M)):
    get_result(M[i],df['productDescription'].loc[M[0]], df['productDescription'].loc[M[i]], df['link'].loc[M[i]], 'bag_of_words')
    print('ID :',df['id'].loc[M[i]])
    print ('Color:', df['baseColour'].loc[M[i]])
    print ('Title:', df['productDescription'].loc[M[i]])
    print ("The distance is: ", D[i])
    print('='*60)

# %%
"""
### Comparing the models
"""

# %%
euclidean_distance=[]
num_results=20
euclidean_distance.append(sum(bag_of_words_euclidean)/num_results)
euclidean_distance.append(sum(tf_idf_euclidean)/num_results)
euclidean_distance.append(sum(idf_euclidean)/num_results)
x=euclidean_distance
y=[]
for i in range(0,47,3):
    y.append(i)

euclidean_distance

# %%
import matplotlib.pyplot as plt
import numpy as np

objects = ('bag_of_words', 'tf_idf', 'idf')
y_pos = np.arange(len(objects))
plt.bar(objects, x)
plt.ylabel('Euclidean Distance')
plt.title('Euclidean Distance Measurement')
plt.savefig('Comparison between clothing models.png')
plt.show()