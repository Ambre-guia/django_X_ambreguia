from django.urls import path
from .views import  ToggleLikeView, ToggleRetweetView, HomePageView, PostDetailView, PostUploadView

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('post/upload/', PostUploadView.as_view(), name='post_upload'),
    
    path('status/<int:post_id>', PostDetailView.as_view(), name='view_post'),

    path('like/<int:tweet_id>/', ToggleLikeView.as_view(), name='toggle_like'),
    path('retweet/<int:tweet_id>/', ToggleRetweetView.as_view(), name='toggle_retweet'),
]
