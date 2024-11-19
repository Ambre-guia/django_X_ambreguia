from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']


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