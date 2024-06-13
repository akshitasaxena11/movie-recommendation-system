# backend/app.py
from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

app = Flask(__name__)

# Load datasets
credits = pd.read_csv("tmdb_5000_credits.csv")
movies = pd.read_csv("tmdb_5000_movies.csv")

# Prepare data
credits_column_renamed = credits.rename(columns={"movie_id": "id"})
movies_merge = movies.merge(credits_column_renamed, on='id')
movies_cleaned = movies_merge.drop(columns=['homepage', 'title_x', 'title_y', 'status', 'production_countries'])
movies_cleaned['overview'] = movies_cleaned['overview'].fillna('')

# TF-IDF Vectorization
tfv = TfidfVectorizer(min_df=3, max_features=None,
                      strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                      ngram_range=(1, 3), stop_words='english')
tfv_matrix = tfv.fit_transform(movies_cleaned['overview'])

# Compute the sigmoid kernel
sig = sigmoid_kernel(tfv_matrix, tfv_matrix)

# Reverse mapping of indices and movie titles
indices = pd.Series(movies_cleaned.index, index=movies_cleaned['original_title']).drop_duplicates()

def give_recommendations(title, sig=sig):
    idx = indices[title]
    sig_scores = list(enumerate(sig[idx]))
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    sig_scores = sig_scores[1:11]
    movie_indices = [i[0] for i in sig_scores]
    return movies_cleaned['original_title'].iloc[movie_indices].tolist()

@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movies_cleaned['original_title'].tolist())

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    movie = data.get('movie')
    recommendations = give_recommendations(movie)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
