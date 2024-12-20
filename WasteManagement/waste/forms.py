from django import forms
from django.contrib.auth import get_user_model  # Dynamically fetch the user model
from .models import WasteReport

User = get_user_model()  # Dynamically assign the user model

class WasteReportForm(forms.ModelForm):
    class Meta:
        model = WasteReport
        fields = ['photo', 'location', 'waste_type', 'description', 'priority', 'contact_information', 'nearby_landmarks', 'latitude', 'longitude']


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))


class SignupForm(forms.ModelForm):
    phone_number = forms.CharField(label='Phone Number', max_length=10, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm password'
    }))

    class Meta:
        model = User  # Use the dynamically fetched user model
        fields = ['email', 'username', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
