from  django.urls import path
from . import views
from django.urls import path,include
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
    path('contact/', contact_message, name='contact_message'),
    path('update_profile/', update_profile, name='update_profile'),
    path('courses/', views.courses_view, name='courses'),
    path('search/', search_results, name='search_results'),
    path('user/<str:username>/', views.user_profile, name='user_profile'), 
    path('profile/<int:user_id>/', profile_view, name='profile'),
    path('search/', search_results, name='search_results'),  
    path('profile/<int:user_id>/', profile_view, name='profile_view'),  
    path('user_profile/<int:user_id>/', user_profile_view, name='user_profile_view'), 
    path('courses/', views.course_list, name='course_list'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),  
    path('meeting-details/', views.meeting_details, name='meeting_details'),
    path('meetings',views.meetings,name='meetings'),
    path('upload_course/', views.upload_course, name='upload_course'),
    path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('course/<int:course_id>/', views.view_course, name='view_course'),
    path('course/<int:course_id>/pdf/<str:file_name>/', views.view_pdf, name='view_pdf'),
    path('course/<int:course_id>/video/<str:file_name>/', views.view_video, name='view_video'),
    path('profile/<int:user_id>/', views.user_profile, name='profile'),
    path('course/<int:course_id>/file/<str:file_name>/', views.view_course_file, name='view_course_file'),
    path('courses', views.course_showcase, name="courses"),
    path('showcase/', views.course_showcase, name='course_showcase'),
    path('course/<int:id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('like/<int:course_id>/', views.like_course, name='like_course'),
    path('cart/<int:course_id>/', views.add_to_cart, name='add_to_cart'),
    path('profile/', views.user_profile, name='user_profile'),
    path('purchase/<int:course_id>/', views.purchase_course, name='purchase_course'),
    path('remove_from_cart/<int:course_id>/', views.remove_from_cart, name='remove_from_cart'),
    

]