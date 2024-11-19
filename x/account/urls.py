from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, custom_login_view, CustomPasswordChangeView, profile_view, deactivate_account

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', custom_login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('<str:username>/', profile_view, name='profile'),
    path('<str:username>/deactivate/', deactivate_account, name='deactivate'),
]
