from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, logout_view, FollowUserView, UnfollowUserView, custom_login_view, CustomPasswordChangeView, profile_view, deactivate_account

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', custom_login_view, name='login'), 
    path('logout/', logout_view, name='logout'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('<str:username>/', profile_view, name='profile'),
    path('<str:username>/deactivate/', deactivate_account, name='deactivate'),
    path('follow/<int:user_id>/',FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
]
