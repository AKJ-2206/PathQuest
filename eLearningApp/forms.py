from django import forms
from .models import Profile
from .models import Course
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'profile_photo']  # Include other fields as necessary
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Write your bio here...'}),
            
        }

# class CourseUploadForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ['title', 'description', 'price', 'category', 'course_image', 'course_file']


class CourseUploadForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'category', 'course_image', 'course_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'course_image': 'Upload an image for your course (optional)',
            'course_file': 'Upload your course content file (optional)',
        }