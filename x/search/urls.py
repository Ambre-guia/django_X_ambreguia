from django.urls import path
from .views import UserSearchView

urlpatterns = [
    path('', UserSearchView.as_view(), name='search_users'),
]

