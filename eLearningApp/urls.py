from  django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name="index"), 
    path('about', views.about, name="about"), 
    path('user_login', views.user_login, name="user_login"),
    path('registration',views.registration,name="registration"),
    path('user_logout/', views.user_logout, name='user_logout'),
]