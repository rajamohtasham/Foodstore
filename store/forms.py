from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-transparent text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Enter username'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'image']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-transparent text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Enter phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 h-24 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-transparent text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Enter address',
                'rows': 3
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-700 dark:text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:font-semibold file:bg-blue-100 file:text-blue-700 dark:file:bg-blue-900 dark:file:text-blue-200 border border-gray-300 dark:border-gray-600 rounded-md bg-gray-50 dark:bg-gray-800'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        if self.user:
            self.user.username = self.cleaned_data['username']
            if commit:
                self.user.save()
        if commit:
            user_profile.save()
        return user_profile
