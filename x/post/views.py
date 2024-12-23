
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View

from .models import Tweet, Like, Retweet
from .forms import PostForm

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'tweets/home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        following_users = self.request.user.following.values_list('followed', flat=True)

        
        tweets_from_following = Tweet.objects.filter(
            Q(user__in=following_users) | Q(user=self.request.user)
        )

        
        # retweeted_tweets = Tweet.objects.filter(
        #     retweets__user=self.request.user
        # )

        retweeted_tweets = Retweet.objects.filter(user=self.request.user)
        retweet_tweets_ids = [retweet.original_tweet.id for retweet in retweeted_tweets]
        retweeted_tweets_queryset = Tweet.objects.filter(id__in=retweet_tweets_ids)

        print(f'retweets query : {retweeted_tweets_queryset}')

        for tweet in retweeted_tweets_queryset:
            tweet.is_retweet = True
        
        all_tweets = (tweets_from_following | retweeted_tweets_queryset).order_by('-created_at')

        context['sorted_posts'] = all_tweets
        context['form'] = PostForm()

        return context


class PostCreateView(LoginRequiredMixin, FormView):
    template_name = 'tweets/home.html'
    form_class = PostForm
    success_url = reverse_lazy('home')  
    login_url = 'login'

    def form_valid(self, form):
        form.instance.user = self.request.user  
        form.save() 
        return super().form_valid(form)


class PostUploadView(LoginRequiredMixin, FormView):
    template_name = 'post/post_upload.html'
    form_class = PostForm
    login_url = 'login'
    success_url = reverse_lazy('home') 

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
    

class PostDetailView(DetailView):
    model = Tweet
    template_name = 'tweets/view_post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


class ToggleLikeView(LoginRequiredMixin, View):
    login_url = 'login' 

    def post(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, id=tweet_id)
        like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
        
        if not created: 
            like.delete()
            liked = False
        else:
            liked = True

        return redirect('home')
    

class ToggleRetweetView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, id=tweet_id)
        retweet, created = Retweet.objects.get_or_create(user=request.user, original_tweet=tweet)
        
        if not created: 
            retweet.delete()
            retweeted = False
        else:
            retweeted = True

        return redirect('home')