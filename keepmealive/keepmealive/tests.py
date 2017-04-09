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
        self.superuser = User.objects.create_superuser(
            username='super',
            email='super@test.com',
            password='superpwd'
        )
    
    """
    Test create user with super user
    """
    def test_create_user_w_super(self):
        url = '/api/auth/token/'
        data = {
            'username': 'super',
            'password': 'superpwd'
        }
        response = self.client.post(url, data, format='json')
        token = response.data['token']
        url_create = '/api/users/'
        header = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(token)
        }
        body = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'newuser@test.com'
        }
        response = self.client.post(url_create, body, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username='newuser').username, 'newuser')
    
    """
    Test create user with a normal user
    """
    def test_create_user_w_user(self):
        url = '/api/auth/token/'
        data = {
            'username': 'test',
            'password': 'testpwd'
        }
        response = self.client.post(url, data, format='json')
        token = response.data['token']
        url_create = '/api/users/'
        header = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(token)
        }
        body = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'newuser@test.com'
        }
        response = self.client.post(url_create, body, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    """
    Test create user with no password
    """
    def test_create_user_wn_password(self):
        url = '/api/auth/token/'
        data = {
            'username': 'super',
            'password': 'superpwd'
        }
        response = self.client.post(url, data, format='json')
        token = response.data['token']
        url_create = '/api/users/'
        header = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(token)
        }
        body = {
            'username': 'newuser',
            'email': 'newuser@test.com'
        }
        response = self.client.post(url_create, body, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    """
    Test create user that already exists
    """
    def test_create_duplicate_user(self):
        url = '/api/auth/token/'
        data = {
            'username': 'super',
            'password': 'superpwd'
        }
        response = self.client.post(url, data, format='json')
        token = response.data['token']
        url_create = '/api/users/'
        header = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(token)
        }
        body = {
            'username': 'test',
            'password': 'testpwd',
            'email': 'newuser@test.com'
        }
        response = self.client.post(url_create, body, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    """
    Test update user properties
    """
    def test_update_user(self):
        url = '/api/auth/token/'
        data = {
            'username': 'super',
            'password': 'superpwd'
        }
        response = self.client.post(url, data, format='json')
        token = response.data['token']
        url_update = '/api/users/?user='+str(self.user.id)
        header = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(token)
        }
        body = {
            'username': 'test2',
            'password': 'testpwd2',
            'email': 'newuser2@test.com',
            'first_name': 'updateName',
            'last_name': 'updateSurname'
        }
        response = self.client.put(url_update, body, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    """
    Test delete user
    """
    def test_delete_user(self):
        url = '/api/auth/token/'
        data = {
            'username': 'super',
            'password': 'superpwd'
        }
        response = self.client.post(url, data, format='json')
        token = response.data['token']
        url_update = '/api/users/?user='+str(self.user.id)
        header = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(token)
        }
        response = self.client.delete(url_update, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    """
    Test get user only if super-admin
    """ 
    def test_get_user_for_super_admin(self):
        url = '/api/auth/token/'
        data = {
            'username': 'test',
            'password': 'testpwd'
        }
        response = self.client.post(url, data, format='json')
        token = response.data['token']
        header = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(token)
        }
        url_get = '/api/users/?user=2'
        response = self.client.get(url_get, **header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
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

