from django.shortcuts import render
from django.contrib.auth.models import User 
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ContactMessage
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile
from .forms import ProfileForm



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

def profile_view(request):
    return render(request, 'User/profile.html', {'user': request.user})

def contact_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Create and save the ContactMessage instance
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Show a success message
        messages.success(request, 'Your message has been sent successfully!')
        
        # Redirect to the homepage or another page
        return redirect('index')  # Adjust the redirect as needed
        
    # If not a POST request, redirect to the contact form or another page
    return redirect('index')

def update_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'User/update_profile.html', {'form': form})

@login_required
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    
    return render(request, 'User/profile.html', {'profile': profile})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        # Handle form data here
        # For example:
        user = request.user
        if user.is_authenticated:
            description = request.POST.get('description', '')
            profile_photo = request.FILES.get('profile_photo', None)

            # Update profile information
            user.profile.description = description
            if profile_photo:
                user.profile.profile_photo = profile_photo
            user.profile.save()

            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'error': 'User not authenticated'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})