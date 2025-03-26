from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Enter address', 'rows': 3}),
        }
