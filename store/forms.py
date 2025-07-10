from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Order

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Username")  # ✅ added username field

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'image']

        widgets = {
            'phone': forms.TextInput(attrs={'class': 'dark:text-white dark:bg-transparent w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:border-indigo-500 sm:text-sm', 'placeholder': 'Enter phone number'}),
            'address': forms.Textarea(attrs={'class': 'dark:text-white dark:bg-transparent w-full h-12 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:border-indigo-500 sm:text-sm', 'placeholder': 'Enter address', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['username'].initial = self.user.username  # pre-fill username

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        if self.user:
            self.user.username = self.cleaned_data['username']
            if commit:
                self.user.save()
        if commit:
            user_profile.save()
        return user_profile

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['transaction_id', 'payment_screenshot']