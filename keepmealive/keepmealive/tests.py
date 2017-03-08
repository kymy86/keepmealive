from rest_framework import status
from rest_framework.test import APITestCase
from folders.models import Folder
from django.contrib.auth.models import User


class AuthorizeTest(APITestCase):

    def setUp(self):
        self.users = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='testpwd'
        )
    def test_authorize_user(self):
        url = '/api/auth/token/'
        data = {
            'username': 'test',
            'password': 'testpwd'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'token')
    
    def test_forgot_password(self):
        #@todo
