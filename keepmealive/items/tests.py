from rest_framework import status
from rest_framework.test import APITestCase
from folders.models import Folder
from items.models import Item
from django.contrib.auth.models import User

class ItemTests(APITestCase):

    def setUp(self):
        self.users = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='testpwd'
        )
        url = '/api/auth/token/'
        data = {
            'username': 'test',
            'password': 'testpwd'
        }
        response = self.client.post(url, data, format='json')
        self.token = response.data['token']

    def test_create_item(self):
        folder = Folder.objects.create(name='test folder', idparent=0)
        url = '/api/items/item/'
        data = {
            "name":"test item",
            "description": "test item description",
            "password": "password",
            "username": "test",
            "email": "test@test.com",
            "folder": folder.id
        }
        header = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(self.token)
        }
        response = self.client.post(url, data, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, 'test item')