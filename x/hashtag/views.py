from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Hashtag
from post.models import Tweet


class HashtagView(LoginRequiredMixin, View):
    template_name = 'hashtags/hashtag_view.html'

    def get(self, request, name):
        if name.startswith('%23'):
            name = name[3:]
        
        
        hashtag = get_object_or_404(Hashtag, name=name.lower())
        
        tweets_with_hashtag = Tweet.objects.filter(hashtags=hashtag)
        
        context = {
            'hashtag': hashtag,
            'tweets': tweets_with_hashtag
        }
        return render(request, self.template_name, context)
