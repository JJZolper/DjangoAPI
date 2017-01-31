from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

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
        Ensure we can create a new user object.
        """
        url = reverse('register')
        data = {'username': 'JJZolper', 'password': 'BlueMarlinOn33!!'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'JJZolper')




