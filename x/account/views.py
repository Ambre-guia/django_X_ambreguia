from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from itertools import chain
from .forms import CustomUserCreationForm, UpdateUserForm
from .models import User, Follow
from post.models import Tweet


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')


class CustomLoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
            return render(request, self.template_name)


class CustomPasswordChangeView(LoginRequiredMixin, View):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('profile')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'view_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_user = self.object
        registration_date = view_user.date_joined
        is_own_profile = self.request.user == view_user

        usersposts = Tweet.objects.filter(user=view_user).order_by('-created_at')
        sorted_usersposts = sorted(
            chain(usersposts),
            key=lambda instance: instance.created_at,
            reverse=True
        )

        profile_form = UpdateUserForm(instance=view_user) if is_own_profile else None
        is_following = self.request.user.following.filter(followed=view_user).exists()

        context.update({
            'sorted_usersposts': sorted_usersposts,
            'registration_date': registration_date,
            'is_own_profile': is_own_profile,
            'profile_form': profile_form,
            'is_following': is_following,
        })

        return context

    def post(self, request, *args, **kwargs):
        view_user = self.get_object()
        if request.user == view_user:
            profile_form = UpdateUserForm(request.POST, instance=view_user)
            if profile_form.is_valid():
                profile_form.save()
        else:
            is_following = request.user.following.filter(followed=view_user).exists()
            if is_following:
                Follow.objects.filter(follower=request.user, followed=view_user).delete()
            else:
                Follow.objects.get_or_create(follower=request.user, followed=view_user)
        return redirect('profile', username=view_user.username)


class DeactivateAccountView(LoginRequiredMixin, View):
    def get(self, request, username):
        if request.user.username != username:
            messages.error(request, "Action non autorisée.")
            return redirect('home')

        return render(request, 'users/confirm_deactivation.html', {'username': username})

    def post(self, request, username):
        if request.user.username != username:
            messages.error(request, "Action non autorisée.")
            return redirect('home')

        user = get_object_or_404(User, username=username)
        user.is_active = False
        user.save()
        messages.success(request, "Votre compte a été désactivé avec succès.")
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
