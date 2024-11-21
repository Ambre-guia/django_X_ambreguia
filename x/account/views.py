from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from itertools import chain

from .forms import CustomUserCreationForm, EmailAuthenticationForm, FollowUsersForm, UpdateUserForm
from .models import User, Follow
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

@login_required
def logout_view(request):
    logout(request)  
    return redirect('login')

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
    
    view_user = get_object_or_404(User, username=username)
    registration_date = view_user.date_joined
    is_own_profile = request.user == view_user 

    
    usersposts = Tweet.objects.filter(user=view_user).order_by('-created_at')
    sorted_usersposts = sorted(
        chain(usersposts),
        key=lambda instance: instance.created_at,
        reverse=True
    )

    profile_form = None
    form = None

    
    if request.user == view_user:
        is_own_profile = True
        profile_form = UpdateUserForm(instance=view_user)
        if request.method == 'POST':
            profile_form = UpdateUserForm(request.POST, instance=view_user)
            if profile_form.is_valid():
                profile_form.save()

    
    is_following = request.user.following.filter(followed=view_user).exists()

    form = None
    if request.user != view_user:
        if request.method == 'POST':
            if form.is_valid():
                if is_following:
                    print("L'uilisateur va se désabonner")
                    request.user.follows.filter(followed=view_user).delete()
                    print("L'uilisateur est désabonné")
                else:
                    request.user.follows.create(followed=view_user)
                return HttpResponseRedirect(request.path)

    context = {
        'sorted_usersposts': sorted_usersposts,
        'view_user': view_user,
        'registration_date': registration_date,
        'is_own_profile': is_own_profile,
        'profile_form': profile_form,
        'form': form,
        'is_following': is_following,  
    }

    return render(request, 'users/profile.html', context)


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

class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        return redirect('profile', username=user_to_follow.username)


class UnfollowUserView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)
        Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
        return redirect('profile', username=user_to_unfollow.username)