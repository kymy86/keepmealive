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

    def test_update_item(self):
        folder = Folder.objects.create(name='test folder', idparent=0)
        item = Item.objects.create(
            name='test',
            password='test',
            username='test',
            folder=folder)
        url = '/api/items/item/'+str(item.id)+"/"
        data = {
            "name" : 'updated test',
            "description":"new description",
            "password": "new test",
            "username": "new test",
            "url": "http://www.test.com",
            "folder": str(folder.id)
        }
        header = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(self.token)
        }
        response = self.client.put(url, data, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.get().name, 'updated test')
        self.assertEqual(Item.objects.get().description, 'new description')
        self.assertEqual(Item.objects.get().pwd, 'new test')
        self.assertEqual(Item.objects.get().username, 'new test')
        self.assertEqual(Item.objects.get().url, 'http://www.test.com')
    
    def test_delete_item(self):
        folder = Folder.objects.create(name='test folder', idparent=0)
        item = Item.objects.create(
            name='test',
            password='test',
            username='test',
            folder=folder)
        url = '/api/items/item/'+str(item.id)+"/" 
        header = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(self.token)
        }
        response = self.client.delete(url, format='json', **header)

