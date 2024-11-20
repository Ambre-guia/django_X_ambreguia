from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Hashtag
from post.models import Tweet

@login_required
def hashtag_view(request, name):
    if name.startswith('%23'):
        name = name[3:]
    hashtag = get_object_or_404(Hashtag, name=name.lower())
    tweets_with_hashtag = Tweet.objects.filter(hashtags=hashtag)
    return render(request, 'hashtags/hashtag_view.html', {'hashtag': hashtag, 'tweets': tweets_with_hashtag})