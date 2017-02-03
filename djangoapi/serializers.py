from django.contrib.auth.models import User
from rest_framework import serializers

from favorites.models import Favorite

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

# Serializers define the API representation.
class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Favorite
        fields = ('access_token', 'reddit_id', 'tag_name')


