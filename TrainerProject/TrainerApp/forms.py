from django import forms

from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = (
            'profile_picture',
            'username',
            'first_name',
            'last_name',
            'department',
            'email',
            'phone_number',
            'password'
        )