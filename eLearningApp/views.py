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
from django.http import Http404
import zipfile
import os
from django.conf import settings
from django.http import FileResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User


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
            return redirect('index')  
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
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('index')  
    return redirect('index')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

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
def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    uploaded_courses = Course.objects.filter(instructor=user)
    profile = user.profile
    liked_courses = profile.liked_courses.all()  # Fetch liked courses
    cart_courses = profile.cart_courses.all()      # Fetch cart courses
    context = {
        'user': user,
        'uploaded_courses': uploaded_courses,
        'liked_courses': liked_courses,  # Add liked courses to context
        'cart_courses': cart_courses,      # Add cart courses to context
    }
    return render(request, 'User/profile.html', context)



  
@login_required
def edit_profile(request):
    return render(request, 'User/edit_profile.html', {'user': request.user})

@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            description = request.POST.get('description', '')
            profile_photo = request.FILES.get('profile_photo', None)
            user.profile.description = description
            if profile_photo:
                user.profile.profile_photo = profile_photo
            user.profile.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'User not authenticated'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def courses_view(request):
    courses = Course.objects.all()
    for course in courses:
        course.stars = range(course.rating)
    return render(request, 'User/index.html', {'courses': courses})



def search_results(request):
    query = request.GET.get('q')
    results = Course.objects.filter(title__icontains=query)  
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
    user = get_object_or_404(User, id=user_id) 
    return render(request, 'user_profile.html', {'user': user})


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})



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
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.instructor:
        raise Http404("You don't have permission to delete this course.") 
    if request.method == 'POST':
        course.delete()
        return redirect('profile', user_id=request.user.id)
    return render(request, 'User/delete_course.html', {'course': course})

@login_required
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
    return render(request, 'User/create_course.html', {'form': form})


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()  
            return redirect('profile', user_id=request.user.id)  
    else:
        form = CourseForm(instance=course)

    return render(request, 'User/edit_course.html', {'form': form, 'course': course})

def view_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course_files = []
    if course.course_files:
        zip_path = course.course_files.path
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            course_files = zip_ref.namelist()
    
    context = {
        'course': course,
        'course_files': course_files,
    }
    return render(request, 'User/course_detail.html', context)
    
def view_pdf(request, course_id, file_name):
    course = get_object_or_404(Course, id=course_id)
    zip_path = os.path.join(settings.MEDIA_ROOT, str(course.file))
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        try:
            pdf_file = zip_ref.open(file_name)
            return FileResponse(pdf_file, content_type='application/pdf')
        except KeyError:
            raise Http404("PDF file not found in the course content.")

def view_video(request, course_id, file_name):
    course = get_object_or_404(Course, id=course_id)
    zip_path = os.path.join(settings.MEDIA_ROOT, str(course.file))
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        try:
            video_file = zip_ref.open(file_name)
            response = FileResponse(video_file, content_type='video/mp4')
            response['Content-Disposition'] = f'inline; filename="{file_name}"'
            return response
        except KeyError:
            raise Http404("Video file not found in the course content.")



def view_course_file(request, course_id, file_name):
    course = get_object_or_404(Course, id=course_id)
    file_path = os.path.join(settings.MEDIA_ROOT, 'course_files', course_id, file_name)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    raise Http404("File not found")




def course_showcase(request):
    courses = Course.objects.all().order_by('-created_at')[:10] 
    return render(request, 'User/course_showcase.html', {'courses': courses})



@login_required
def purchase_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user not in course.buyers.all():
        course.buyers.add(request.user)
        course.cart_users.remove(request.user)  
    return redirect('view_course', course_id=course_id)


@login_required
def user_profile(request):
    user = request.user
    liked_courses = user.liked_courses.all()
    cart_courses = user.cart_courses.all()
    purchased_courses = user.purchased_courses.all()
    return render(request, 'User/profile.html', {
        'liked_courses': liked_courses,
        'cart_courses': cart_courses,
        'purchased_courses': purchased_courses
    })



def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'course_detail.html', {'course': course})

from django.contrib.auth.admin import UserAdmin
class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        print("Saving user:", obj)
        super().save_model(request, obj, form, change)


from django.contrib import admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)







from .models import Course, Profile


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    context = {
        'course': course,
        'is_liked': request.user in course.likers.all() if request.user.is_authenticated else False,
        'in_cart': request.user in course.cart_users.all() if request.user.is_authenticated else False,
    }
    return render(request, 'course_detail.html', context)

@login_required
def like_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    if user in course.likers.all():
        course.likers.remove(user)
        liked = False
    else:
        course.likers.add(user)
        liked = True
    return JsonResponse({'liked': liked})

@login_required
def add_to_cart(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    if user in course.cart_users.all():
        course.cart_users.remove(user)
        in_cart = False
    else:
        course.cart_users.add(user)
        in_cart = True
    return JsonResponse({'in_cart': in_cart})

@login_required
def user_profile(request):
    user = request.user
    liked_courses = user.liked_courses.all()
    cart_courses = user.cart_courses.all()
    purchased_courses = user.purchased_courses.all()
    context = {
        'liked_courses': liked_courses,
        'cart_courses': cart_courses,
        'purchased_courses': purchased_courses,
    }
    return render(request, 'user_profile.html', context)

@login_required
def remove_from_cart(request, course_id):
    # Get the course that the user wants to remove
    course = get_object_or_404(Course, id=course_id)
    
    # Assuming the Course model has a many-to-many field with the User model for the cart
    if request.user in course.cart_users.all():
        course.cart_users.remove(request.user)  # Remove the user from the cart_users for that course
    
    # Redirect to the course detail page or the cart page
    return redirect('view_cart')  # Adjust 'view_cart' to your actual cart page URL name