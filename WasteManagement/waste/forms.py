from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError


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
        model = CustomUser
        fields = ['email', 'username', 'phone_number']

   
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Save hashed password
        if commit:
            user.save()
        return user

# Commented out forms
# class ReportIssueForm(forms.ModelForm):
#     class Meta:
#         model = WasteIssue
#         fields = ['issue_type', 'description', 'location']

# class RequestPickupForm(forms.ModelForm):
#     class Meta:
#         model = PickupRequest
#         fields = ['item_description', 'location']

# class AddImageForm(forms.ModelForm):
#     class Meta:
#         model = UserImage
#         fields = ['image']

# class UpdateIssueForm(forms.ModelForm):
#     class Meta:
#         model = WasteIssue
#         fields = ['status']
# 
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['status'].label = 'New Status'
