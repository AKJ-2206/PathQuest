import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from eLearningApp.models import Course
import joblib

def train_model():
    # Fetch all courses from the database
    courses = Course.objects.all()
    
    # Convert queryset to dataframe
    df = pd.read_csv("Course_info.csv")
    
    # Combine relevant text fields
    df['combined_features'] = df['title'] + ' ' + df['headline'] + ' ' + df['category'] + ' ' + df['subcategory'] + ' ' + df['topic']
    
    # Create TF-IDF vectorizer
    tfidf = TfidfVectorizer(stop_words='english')
    
    # Fit and transform the combined features
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    
    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # Save the model and similarity matrix
    joblib.dump(tfidf, 'recommender/tfidf_vectorizer.joblib')
    np.save('recommender/cosine_sim.npy', cosine_sim)
    
    # Save course indices
    course_indices = pd.Series(df.index, index=df['id']).to_dict()
    joblib.dump(course_indices, 'recommender/course_indices.joblib')

if __name__ == '__main__':
    train_model()