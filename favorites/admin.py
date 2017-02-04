from django.contrib import admin

from favorites.models import Favorite, RedditPost

admin.site.register(Favorite)
admin.site.register(RedditPost)

