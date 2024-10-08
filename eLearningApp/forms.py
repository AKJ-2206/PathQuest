from django import forms
from .models import Profile
from .models import Course
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'profile_photo']  
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Write your bio here...'}),
            
        }


from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price','cover_image','content_upload']