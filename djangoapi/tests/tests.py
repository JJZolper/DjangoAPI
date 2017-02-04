from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from favorites.models import Favorite, RedditPost

class UserTests(APITestCase):

    def test_register(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('register')
        data = {'username': 'JJZolper', 'password': 'BlueMarlinOn33!!'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'JJZolper')

    def test_login(self):
        """
        Ensure we can login a user object.
        """
        self.test_register()
        url = reverse('login')
        data = {'username': 'JJZolper', 'password': 'BlueMarlinOn33!!'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reddit(self):
        """
        Ensure we can login a user object.
        """
        self.test_register()
        url = reverse('reddit')
        user = User.objects.get(username__iexact='JJZolper')
        token = Token.objects.get(user_id=user.id)
        data = {'access_token': token.key}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_favorite(self):
        """
        Ensure we can login a user object.
        """
        self.test_reddit()
        url = reverse('favorite')
        user = User.objects.get(username__iexact='JJZolper')
        token = Token.objects.get(user_id=user.id)
        redditpost = RedditPost.objects.all()
        data = {'access_token': token.key, 'tag_name': 'funny', 'reddit_id': redditpost[0].reddit_id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_favorites(self):
        """
        Ensure we can login a user object.
        """
        self.test_favorite()
        url = reverse('favorites')
        user = User.objects.get(username__iexact='JJZolper')
        token = Token.objects.get(user_id=user.id)
        data = {'access_token': token.key}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tag(self):
        """
        Ensure we can login a user object.
        """
        self.test_favorite()
        url = reverse('tag')
        user = User.objects.get(username__iexact='JJZolper')
        token = Token.objects.get(user_id=user.id)
        data = {'access_token': token.key, 'tag_name': 'funny'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


