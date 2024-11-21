from django.urls import path
from .views import (
    RegisterView, LogoutView, CustomLoginView, ProfileView,
    DeactivateAccountView, FollowUserView, UnfollowUserView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/<slug:username>/', ProfileView.as_view(), name='profile'),
    path('deactivate/<slug:username>/', DeactivateAccountView.as_view(), name='deactivate_account'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
]
