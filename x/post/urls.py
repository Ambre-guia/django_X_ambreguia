from django.urls import path
from . import views 

urlpatterns = [
    path('home/', views.homepage, name='home'),
    path('post/upload/', views.post_upload, name='post_upload'),
    
    path('status/<int:post_id>', views.view_post, name='view_post'),

    path('like/<int:tweet_id>/', views.toggle_like, name='toggle_like'),
    path('retweet/<int:tweet_id>/', views.toggle_retweet, name='toggle_retweet'),
]
