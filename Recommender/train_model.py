import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from scipy.sparse import hstack

def train_model(data_path):
    # Load the dataset
    df = pd.read_csv(data_path)
    
    # Preprocess the data
    le = LabelEncoder()
    df['category'] = le.fit_transform(df['category'].fillna('Unknown'))
    df['subcategory'] = le.fit_transform(df['subcategory'].fillna('Unknown'))
    df['topic'] = le.fit_transform(df['topic'].fillna('Unknown'))
    df['language'] = le.fit_transform(df['language'].fillna('Unknown'))
    
    # Create a feature vector
    features = ['category', 'subcategory', 'topic', 'language', 'is_paid', 'price', 'num_subscribers', 'avg_rating', 'num_reviews', 'num_lectures', 'content_length_min']
    X = df[features].fillna(0)  # Fill NaN values with 0 for numerical features
    
    # Combine text features and handle NaN values
    df['text_features'] = df['title'].fillna('') + ' ' + df['headline'].fillna('')
    
    # Create TF-IDF vectors from text features
    tfidf = TfidfVectorizer(stop_words='english', max_features=10000)  # Limit the number of features
    tfidf_matrix = tfidf.fit_transform(df['text_features'])
    
    # Convert X.values to float to ensure compatibility with sparse matrix
    combined_features = hstack([X.values.astype(float), tfidf_matrix])  # Keep the tfidf_matrix sparse
    
    # Create models directory if it doesn't exist
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Save the model components
    joblib.dump(le, os.path.join(models_dir, 'label_encoder.joblib'))
    joblib.dump(tfidf, os.path.join(models_dir, 'tfidf_vectorizer.joblib'))
    joblib.dump(combined_features, os.path.join(models_dir, 'combined_features.joblib'))  # Save the sparse matrix
    df[['id', 'title', 'instructor_name', 'course_url']].to_csv(os.path.join(models_dir, 'course_info.csv'), index=False)
    
    print("Model training completed and saved.")

if __name__ == "__main__":
    train_model('/Volumes/Coding2/tri4e/Project/prototype3/PathQuest/recommender/Course_info1.csv')
