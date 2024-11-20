from django.db.models.signals import post_save
from django.dispatch import receiver

from post.models import Tweet

from .models import Hashtag
from .utils import extract_hashtags 

@receiver(post_save, sender=Tweet)
def handle_hashtags(sender, instance, **kwargs):
    hashtags = extract_hashtags(instance.content)
    for tag in hashtags:
        hashtag_obj, created = Hashtag.objects.get_or_create(name=tag.lower())
        instance.hashtags.add(hashtag_obj)
