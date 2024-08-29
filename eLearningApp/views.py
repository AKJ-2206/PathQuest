from django.shortcuts import render
from django.contrib.auth.models import User 

def index(request):
    return render(request, 'User/index.html')

def about(request):
    return render(request, 'User/about.html')

def login(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    return render(request, 'User/login.html')

def registration(request):
    return render(request,'User/registration.html')
