from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Favorite
class Favorite(models.Model):
    user = models.ForeignKey(User)
    access_token = models.CharField(max_length=100, default="")
    reddit_id = models.CharField(max_length=100, default="")
    permalink = models.CharField(max_length=250, default="")
    url = models.CharField(max_length=250, default="")
    author = models.CharField(max_length=100, default="")
    tag_name = models.CharField(max_length=100, default="")

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'

    def __str__(self):
        return str(self.reddit_id)

# Reddit Post
class RedditPost(models.Model):
    reddit_id = models.CharField(max_length=100, default="")
    permalink = models.CharField(max_length=250, default="")
    url = models.CharField(max_length=250, default="")
    author = models.CharField(max_length=100, default="")

    class Meta:
        verbose_name = 'Reddit Post'
        verbose_name_plural = 'Reddit Posts'

    def __str__(self):
        return str(self.reddit_id)




