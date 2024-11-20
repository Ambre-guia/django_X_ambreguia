from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Hashtag
from post.models import Tweet

def hashtag_view(request, name):
    hashtag = get_object_or_404(Hashtag, name=name)
    tweets_with_hashtag = Tweet.objects.filter(hashtags=hashtag)
    return render(request, 'hashtags/hashtag_view.html', {'hashtag': hashtag, 'tweets': tweets_with_hashtag})