from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'profile_photo']  # Include other fields as necessary
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Write your bio here...'}),
        }