import numpy as np
import joblib
from eLearningApp.models import Course

def get_recommendations(course_id, top_n=5):
    # Load the saved model and data
    cosine_sim = np.load('recommender/cosine_sim.npy')
    course_indices = joblib.load('recommender/course_indices.joblib')
    
    # Get the index of the course
    idx = course_indices[course_id]
    
    # Get the pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort the courses based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get the scores of the top_n most similar courses
    sim_scores = sim_scores[1:top_n+1]
    
    # Get the course indices
    course_indices = [i[0] for i in sim_scores]
    
    # Return the top most similar courses
    return Course.objects.filter(id__in=course_indices)

def get_personalized_recommendations(user, top_n=5):
    # Get the courses the user has taken
    taken_courses = user.userprofile.courses_taken.all()
    
    # If the user hasn't taken any courses, return popular courses
    if not taken_courses:
        return Course.objects.order_by('-num_subscribers')[:top_n]
    
    # Get recommendations for each course the user has taken
    all_recommendations = []
    for course in taken_courses:
        recommendations = get_recommendations(course.id, top_n)
        all_recommendations.extend(recommendations)
    
    # Remove duplicates and sort by number of subscribers
    unique_recommendations = list(set(all_recommendations))
    unique_recommendations.sort(key=lambda x: x.num_subscribers, reverse=True)
    
    # Return the top N recommendations
    return unique_recommendations[:top_n]