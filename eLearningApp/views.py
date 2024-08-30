from django.shortcuts import render
from django.contrib.auth.models import User 
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
    return render(request, 'User/index.html')

def about(request):
    return render(request, 'User/about.html')

def user_login(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'User/index.html')
    return render(request, 'User/login.html')

# def registration(request):
#     return render(request,'User/registration.html')
def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(first_name = first_name, last_name = last_name, username = username, email = email)
        user.set_password(password)
        user.save()
        return render(request, 'User/index.html')
    return render(request, 'User/registration.html')

def user_logout(request):
    logout(request)
    return render(request, 'User/login.html')
