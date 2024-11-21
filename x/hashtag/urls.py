from django.urls import path
from .views import HashtagView

urlpatterns = [
    path('hashtag/<str:name>/', HashtagView.as_view(), name='hashtag_view'),
]
