from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser): 
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
            'auth.Group',
            related_name='account_user_set',
            blank=True,
            help_text='The groups this user belongs to.'
        )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='account_user_permissions_set',  
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower} follows {self.followed}"