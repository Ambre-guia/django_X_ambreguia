from django.db import models
from account.models  import User
from hashtag.models import Hashtag

from hashtag.utils import extract_hashtags

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    content = models.TextField(max_length=280)
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name='tweets')

    image = models.ImageField(upload_to='tweet_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Sauvegarde le tweet
        self.update_hashtags()

    def update_hashtags(self):
        hashtags = extract_hashtags(self.content)
        for tag in hashtags:
            hashtag_obj, created = Hashtag.objects.get_or_create(name=tag.lower())
            self.hashtags.add(hashtag_obj)
    
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet')

    def __str__(self):
        return f"{self.user} likes {self.tweet}"
    
class Retweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="retweets")
    original_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="retweets")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} retweeted {self.original_tweet}"