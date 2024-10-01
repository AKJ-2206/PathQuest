from  django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import contact_message, update_profile, profile_view 
from django.conf import settings
from django.conf.urls.static import static
from .views import  search_results, profile_view, user_profile_view

urlpatterns = [
    path('', views.index, name="index"), 
    path('about', views.about, name="about"), 
    path('user_login', views.user_login, name="user_login"),
    path('registration',views.registration,name="registration"),
    path('user_logout/', views.user_logout, name='user_logout'),
    # path('profile/', views.profile_view, name='profile'),
    path('contact/', contact_message, name='contact_message'),
    path('update_profile/', update_profile, name='update_profile'),
    # path('profile/', profile_view, name='profile'),
    path('courses/', views.courses_view, name='courses'),
    # path('search/', views.search_results, name='search_results'),
    path('search/', search_results, name='search_results'),
     path('user/<str:username>/', views.user_profile, name='user_profile'), 
      path('profile/<int:user_id>/', profile_view, name='profile'),
    path('search/', search_results, name='search_results'),  # Add search results URL
    path('profile/<int:user_id>/', profile_view, name='profile_view'),  # Add editable profile view URL
    path('user_profile/<int:user_id>/', user_profile_view, name='user_profile_view'),  # Add user profile view URL
    #  path('courses/', views.course_list, name='course_list'),
     path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('upload_course/', views.upload_course, name='upload_course'),
]