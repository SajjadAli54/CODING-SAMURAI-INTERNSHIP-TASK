import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the data
data_path = "./data/Dataset.csv"
title_path = "./data/Movie_Id_Titles.csv"

ratings_df = pd.read_csv(data_path)
movies_df = pd.read_csv(title_path)

# Load the model
model_path = "./recommender.pkl"
model_knn = joblib.load(model_path)

# Merge movies and ratings data
movie_data = pd.merge(ratings_df, movies_df, on='item_id')

# Create a pivot table of user ratings
movie_ratings = movie_data.pivot_table(
    index='user_id', columns='title', values='rating')

# Fill missing values with 0 (assuming no rating means a rating of 0)
movie_ratings = movie_ratings.fillna(0)

# Convert the pivot table to a dense matrix
movie_ratings_matrix = movie_ratings.values

# Calculate cosine similarity between movies based on user ratings
cosine_sim = cosine_similarity(movie_ratings_matrix, movie_ratings_matrix)

# Create a mapping of movie titles to their respective indices
movie_indices = pd.Series(movies_df.index, index=movies_df['title'])


# Function to get movie recommendations
def get_movie_recommendations(movie_title, num_recommendations=10):
    movie_id = movies_df.loc[movies_df['title']
                             == movie_title]['item_id'].values[0]
    distances, indices = model_knn.kneighbors(
        movie_ratings.iloc[movie_id - 1, :].values.reshape(1, -1), n_neighbors=num_recommendations + 1)
    recommended_movie_indices = [i + 1 for i in indices.flatten()]
    recommended_movies = [movies_df.loc[movies_df['item_id'] == idx]
                          ['title'].values[0] for idx in recommended_movie_indices][1:]
    return recommended_movies
