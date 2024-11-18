from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm
from .models import User


@csrf_exempt
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
        messages.error(request, "Action non autorisée.")
        return redirect('home')
    
    try:
        user = User.objects.get(username=username)
        user.is_active = False
        user.save()
        messages.success(request, "Votre compte a été désactivé avec succès.")
    except User.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"Une erreur est survenue : {e}")
        return redirect('home')

    return redirect('logout')