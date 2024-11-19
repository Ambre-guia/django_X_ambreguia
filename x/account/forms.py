from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))


#################
### REFLEXION ###
#################

#class UpdateUserForm(forms.ModelForm):
#    class Meta:
#        model = User
#        fields = ['first_name', 'last_name', 'bio']

#class FollowUsersForm(forms.ModelForm):
#    class Meta:
#        model = User
#        fields = ['follows']