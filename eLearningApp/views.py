from django.shortcuts import render, get_object_or_404
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
from .models import Course
from django.db import IntegrityError
from .forms import CourseForm

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



def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, 'User/registration.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email address.")
            return render(request, 'User/registration.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')  
        except IntegrityError as e:
            messages.error(request, f"An error occurred during registration: {str(e)}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

    return render(request, 'User/registration.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to your home page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'User/login.html')


def user_logout(request):
    logout(request)
    return render(request, 'User/login.html')


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
def profile_view(request,user_id):
    try:
        profile = Profile.objects.get(user=user_id)
    except Profile.DoesNotExist:
        profile = None
    
    return render(request, 'User/profile.html', {'profile': profile})




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
  
@login_required
def edit_profile(request):
    return render(request, 'User/edit_profile.html', {'user': request.user})

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


def courses_view(request):
    courses = Course.objects.all()

    # Prepare courses data with stars
    for course in courses:
        course.stars = range(course.rating)

    return render(request, 'User/index.html', {'courses': courses})



def search_results(request):
    query = request.GET.get('q')
    results = Course.objects.filter(title__icontains=query)  # Make sure this line refers to 'title'
    return render(request, 'User/search_results.html', {'results': results})

    
    return render(request, 'User/search_results.html', {
        'query': query,
        'course_results': course_results,
        'user_results': user_results,
    })


@login_required
def user_profile(request):
    user = request.user
    return render(request, 'User/profile.html', {'user': user})

def user_profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Fetch the user by ID
    return render(request, 'user_profile.html', {'user': user})


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})

def meeting_details(request):
    return render(request, 'User/meeting-details.html')


def meetings(request):
    return render(request, 'User/meetings.html')

@login_required
def upload_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user  
            course.save()  
            return redirect('profile',request.user.id)  
    else:
        form = CourseForm()  
        

   
    return render(request, 'User/upload_course.html', {'form': form})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'edit_course.html', {'form': form, 'course': course})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('profile')  # or wherever you want to redirect after deletion
    return render(request, 'delete_course.html', {'course': course})

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'edit_course.html', {'form': form, 'course': course})
