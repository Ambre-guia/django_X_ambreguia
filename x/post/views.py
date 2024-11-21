from itertools import chain
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from . import models
from . import forms

@login_required
def homepage(request):
    form = forms.PostForm()
    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            
            form.instance.user = request.user
            post = form.save(commit=False)
           
            post.user = request.user
            
            post.save()
            return redirect('home')
        
   


    posts = models.Tweet.objects.filter(user=request.user).order_by('-created_at')
    sorted_posts = sorted(
        chain(posts),
        key=lambda instance: instance.created_at,
        reverse=True
    )

    context = {
        'sorted_posts': posts,

        'form': form
    }

    return render(request, 'tweets/home.html', context=context)

@login_required
def post_upload(request):
    form = forms.PostForm()
    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            post = form.save(commit=False)
            
            post.user = request.user
            
            post.save()
            return redirect('home')
    return render(request, 'post/post_upload.html', context={'form': form})

@login_required
def view_post(request, post_id):

    post = get_object_or_404(models.Tweet, id=post_id)

    # comments = models.Comment.objects.filter(post=post)
    # sorted_comments = sorted(
    #     chain(comments),
    #     key=lambda instance: instance.date_created,
    #     reverse=True
    # )


    # form = forms.CommentForm()
    # if request.method == 'POST':
    #     form = forms.CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.post = post  
    #         comment.uploader = request.user 
            
    #         form.save()
    #         return redirect('view_post', post_id=post.id)
        
    context = {
            'post': post,
            # 'sorted_comments' : sorted_comments
        }
    
    return render(request, 'tweets/view_post.html', context=context)

@login_required
def toggle_like(request, tweet_id):
    tweet = get_object_or_404(models.Tweet, id=tweet_id)
    like, created = models.Like.objects.get_or_create(user=request.user, tweet=tweet)
    if not created:
        # Si un like existe déjà, le supprimer
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'likes_count': tweet.likes.count()})

@login_required
def toggle_retweet(request, tweet_id):
    tweet = get_object_or_404(models.Tweet, id=tweet_id)
    retweet, created = models.Retweet.objects.get_or_create(user=request.user, original_tweet=tweet)
    if not created:
        # Si un retweet existe déjà, le supprimer
        retweet.delete()
        retweeted = False
    else:
        retweeted = True

    return JsonResponse({'retweeted': retweeted, 'retweets_count': tweet.retweets.count()})