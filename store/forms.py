from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:border-indigo-500 sm:text-sm' 'form-input', 'placeholder': 'Enter phone number'}),
            'address': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:border-indigo-500 sm:text-sm' 'form-textarea', 'placeholder': 'Enter address', 'rows': 3}),
        }
