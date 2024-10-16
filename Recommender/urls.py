# recommender/urls.py
from django.urls import path
from . import views

app_name = 'recommender'

urlpatterns = [
    path('', views.course_recommendations, name='recommendations'),

]