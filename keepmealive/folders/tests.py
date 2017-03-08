from rest_framework import status
from rest_framework.test import APITestCase
from folders.models import Folder
from django.contrib.auth.models import User

class FolderTests(APITestCase):

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

    def test_create_folder(self):
        url = '/api/folders/folder/'
        data = {
            'name': 'test folder',
            'idparent': 0,
        }
        header = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(self.token)
        }
        response = self.client.post(url, data, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Folder.objects.count(), 1)
        self.assertEqual(Folder.objects.get().name, 'test folder')

    def test_update_folder(self):

        folder = Folder.objects.create(name='test folder', idparent=0)
        url = '/api/folders/folder/'+str(folder.id)+"/"
        data = {
            'name': 'Test folder updated',
            'idparent': str(folder.idparent)
        }
        header = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(self.token)
        }
        response = self.client.put(url, data, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Folder.objects.get().name, 'Test folder updated')

    def test_delete_folder(self):
        folder = Folder.objects.create(name='test folder', idparent=0)
        url = '/api/folders/folder/'+str(folder.id)+"/"
        header = {
            'HTTP_AUTHORIZATION': 'JWT {}'.format(self.token)
        }
        response = self.client.delete(url, format='json', **header)
