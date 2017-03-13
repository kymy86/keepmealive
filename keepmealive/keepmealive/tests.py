from rest_framework import status
from rest_framework.test import APITestCase
from folders.models import Folder
from keepmealive.models import PasswordForgotRequest
from django.contrib.auth.models import User


class AuthorizeTest(APITestCase):

    """
    Create a new user
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='testpwd'
        )
    
    """
    Test right authentication
    """
    def test_authorize_user(self):
        url = '/api/auth/token/'
        data = {
            'username': 'test',
            'password': 'testpwd'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'token')
    
    """
    Raise an error if user doesn't specify
    a username
    """
    def test_forgot_password_wno_username(self):
        url = '/api/users/forgot/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    """
    Test if an hash is generated when the
    right username is provided
    """
    def test_forgot_password(self):
        url = '/api/users/forgot/?username=test'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(PasswordForgotRequest.objects.get().user.id, self.user.id)
    
    """
    Raise an error if a wrong hash is provided
    """
    def test_reset_password_with_wrong_hash(self):
        url = '/api/users/reset/'
        data = {
            'hash': '91581ada-4aa4-4ad2-9a63-53486707a735',
            'email': 'test@test.com',
            'password': 'test2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    """
    Raise error if the email provided
    is different from the owner email
    """
    def test_reset_password_with_wrong_email(self):
        url = '/api/users/reset/'
        response = self.client.get('/api/users/forgot/?username=test', format='json')
        pwdmodel = PasswordForgotRequest.objects.get(user_id=self.user.id)
        data = {
            'hash': pwdmodel.hash,
            'email': 'test@testxs.com',
            'password': 'test2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    """
    Test the reset password procedure
    """
    def test_reset_password(self):
        url = '/api/users/reset/'
        response = self.client.get('/api/users/forgot/?username=test', format='json')
        pwdmodel = PasswordForgotRequest.objects.get(user_id=self.user.id)
        data = {
            'hash': pwdmodel.hash,
            'email': self.user.email,
            'password': 'test22'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(PasswordForgotRequest.objects.get(hash=pwdmodel.hash).used)
        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password('test22'))

