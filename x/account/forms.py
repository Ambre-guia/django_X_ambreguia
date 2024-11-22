from django.contrib.auth.forms import UserCreationForm
from .models import User, Follow
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))


class UpdateUserForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['bio', 'profile_picture']

class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ['followed']