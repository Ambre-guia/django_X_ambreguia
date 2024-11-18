from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .forms import CustomUserCreationForm

from django.contrib.auth.views import LoginView, PasswordChangeView

from django.urls import reverse_lazy
from .models import User

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('profile')
    
@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'users/profile.html', {'user': user})

@login_required
def deactivate_account(request, username):
    if request.user.username != username:
        return redirect('home')
    user = get_object_or_404(User, username=username)
    user.is_active = False
    user.save()
    return redirect('logout')