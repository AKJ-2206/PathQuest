# recommender/views.py
from django.shortcuts import render
from .models import UserProfile
from .recommender import CourseRecommender

def course_recommendations(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    recommendations = CourseRecommender.get_recommendations(user_profile.interests)
    return render(request, 'recommender/recommendations.html', {'recommendations': recommendations})


