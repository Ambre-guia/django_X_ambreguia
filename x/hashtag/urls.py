from django.urls import path
from . import views

urlpatterns = [
    path('<str:name>/', views.hashtag_view, name='hashtag_view'),
]