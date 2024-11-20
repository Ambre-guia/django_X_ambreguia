from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.urls import reverse_lazy
from itertools import chain

from .forms import CustomUserCreationForm, EmailAuthenticationForm
from .models import User
from post.models import Tweet


@csrf_exempt
def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.uploader = request.user
            user = form.save()
            login(request, user)  
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def custom_login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
            return render(request, 'users/login.html')  
    else:
        return render(request, 'users/login.html')  

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('profile')
    
@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    registration_date = user.date_joined
    user = request.user
    usersposts = Tweet.objects.filter(user=request.user).order_by('-created_at')
    sorted_usersposts = sorted(
        chain(usersposts),
        key=lambda instance: instance.created_at,
        reverse=True
    )

    return render(request, 'users/profile.html', {'user': user,
            'registration_date': registration_date,
            'sorted_usersposts': sorted_usersposts,
            })

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