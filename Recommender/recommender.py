import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from scipy.sparse import hstack  # Ensure this import is included

class CourseRecommender:
    def __init__(self):
        self.models_dir = os.path.join(os.path.dirname(__file__), 'models')
        self.le = None
        self.tfidf = None
        self.combined_features = None
        self.course_info = None

    def train_model(self, data_path):
        # Load the dataset
        df = pd.read_csv(data_path)

        # Preprocess the data
        self.le = LabelEncoder()
        df['category'] = self.le.fit_transform(df['category'].fillna('Unknown'))
        df['subcategory'] = self.le.fit_transform(df['subcategory'].fillna('Unknown'))
        df['topic'] = self.le.fit_transform(df['topic'].fillna('Unknown'))
        df['language'] = self.le.fit_transform(df['language'].fillna('Unknown'))
        
        # Create a feature vector
        features = ['category', 'subcategory', 'topic', 'language', 'is_paid', 'price', 'num_subscribers', 'avg_rating', 'num_reviews', 'num_lectures', 'content_length_min']
        X = df[features].fillna(0)  # Fill NaN values with 0 for numerical features
        
        # Combine text features and handle NaN values
        df['text_features'] = df['title'].fillna('') + ' ' + df['headline'].fillna('')
        df['text_features'] = df['text_features'].fillna('')  # Replace NaN with empty string
        
        # Create TF-IDF vectors from text features
        self.tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = self.tfidf.fit_transform(df['text_features'])

        # Combine numerical and text features
        self.combined_features = hstack((X.values, tfidf_matrix))  # Use hstack for sparse matrices

        # Create models directory if it doesn't exist
        os.makedirs(self.models_dir, exist_ok=True)

        # Save the model components
        joblib.dump(self.le, os.path.join(self.models_dir, 'label_encoder.joblib'))
        joblib.dump(self.tfidf, os.path.join(self.models_dir, 'tfidf_vectorizer.joblib'))
        joblib.dump(self.combined_features, os.path.join(self.models_dir, 'combined_features_sparse.joblib'))  # Save the sparse matrix
        df[['id', 'title', 'instructor_name', 'course_url']].to_csv(os.path.join(self.models_dir, 'course_info.csv'), index=False)

        print("Model training completed and saved.")

    def load_model(self):
        self.le = joblib.load(os.path.join(self.models_dir, 'label_encoder.joblib'))
        self.tfidf = joblib.load(os.path.join(self.models_dir, 'tfidf_vectorizer.joblib'))
        self.combined_features = joblib.load(os.path.join(self.models_dir, 'combined_features_sparse.joblib'))  # Load the sparse matrix
        self.course_info = pd.read_csv(os.path.join(self.models_dir, 'course_info.csv'))

    def get_recommendations(self, user_interests, num_recommendations=5):
        if self.tfidf is None or self.combined_features is None or self.course_info is None:
            self.load_model()

        # Transform user interests
        user_vector = self.tfidf.transform([user_interests])
        # Ensure the user_vector has the same shape as combined_features
        user_vector = hstack([np.zeros((1, self.combined_features.shape[1] - user_vector.shape[1])), user_vector])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(user_vector, self.combined_features)
        
        # Get top recommendations
        top_indices = similarities[0].argsort()[-num_recommendations:][::-1]
        recommendations = self.course_info.iloc[top_indices]
        
        return recommendations.to_dict('records')
