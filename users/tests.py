from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from rest_framework.test import APITestCase
from rest_framework import status

import datetime as dt

from .serializers import UserDetailsSerializer

User = get_user_model()


class UserTests(TestCase):

    def test_normal_user(self):
        """
        Test creation of a normal user with username / password.
        """
        today = dt.datetime.today()

        test = User.objects.create_user(
            username='test', password='123Testtest123')

        self.assertEqual(test.username, 'test')
        self.assertTrue(test.check_password('123Testtest123'))
        self.assertFalse(test.is_staff)
        self.assertFalse(test.is_superuser)
        self.assertTrue(test.is_active)
        self.assertTrue(test.uuid)
        self.assertEqual(test.date_joined.day, today.day)
        self.assertEqual(test.date_joined.month, today.month)
        self.assertEqual(test.date_joined.year, today.year)

    def test_superuser(self):
        """
        Test superuser creation with custom user model.
        """
        today = dt.datetime.today()

        test = User.objects.create_superuser(
            username='test', password='123Testtest123')

        self.assertEqual(test.username, 'test')
        self.assertTrue(test.check_password('123Testtest123'))
        self.assertTrue(test.is_staff)
        self.assertTrue(test.is_superuser)
        self.assertTrue(test.is_active)
        self.assertTrue(test.uuid)
        self.assertEqual(test.date_joined.day, today.day)
        self.assertEqual(test.date_joined.month, today.month)
        self.assertEqual(test.date_joined.year, today.year)

    def test_username_unqiue(self):
        """
        Assert that usernames must be unique.
        """
        with self.assertRaises(IntegrityError):
            u1 = User.objects.create_user(
                username='user1', password='123Testtest123')
            u2 = User.objects.create_user(
                username='user1', password='123Testtest123')


class TestUserApi(APITestCase):

    def _register_user(self):
        return self.client.post('/auth/register/', data={
            'username': 'test',
            'password1': '123tester123',
            'password2': '123tester123',
        }, format='json')

    def test_user_registration(self):
        res = self._register_user()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username='test')
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('123tester123'))

    def test_same_username(self):
        self._register_user()
        res = self._register_user()
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_diff_passwords(self):
        res = self.client.post('/auth/register/', data={
            'username': 'test',
            'password1': '123tester',
            'password2': '123tester123',
        }, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        count = User.objects.all().count()
        self.assertEqual(count, 0)

    def test_user_login(self):
        res = self._register_user()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.post('/auth/login/', data={
            'username': 'test',
            'password': '123tester123',
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['access'])
        self.assertTrue(res.data['refresh'])

    def test_bad_login(self):
        res = self.client.post('/auth/login/', data={
            'username': 'test',
            'password': '123tester123',
        })
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bad_creds(self):
        res = self._register_user()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.post('/auth/login/', data={
            'username': 'test',
            'password': 'wrong_password',
        })
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_details(self):
        res = self._register_user()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # login
        res = self.client.post('/auth/login/', data={
            'username': 'test',
            'password': '123tester123',
        })

        user = User.objects.get(username='test')
        user_data = UserDetailsSerializer(instance=user)

        res = self.client.get('/auth/user/', HTTP_AUTHORIZATION=f'Bearer {res.data["access"]}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, user_data.data)

    def test_user_details_username(self):
        res = self._register_user()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username='test')
        user_data = UserDetailsSerializer(instance=user)

        res = self.client.get('/auth/user/test/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, user_data.data)

    def test_password_change(self):
        res = self._register_user()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # login
        res = self.client.post('/auth/login/', data={
            'username': 'test',
            'password': '123tester123',
        })
        token = res.data["access"]

        res = self.client.post('/auth/password/change/',
                               data={
                                   'password1': 'newpassword',
                                   'password2': 'newpassword',
                               },
                               format='json',
                               HTTP_AUTHORIZATION=f'Bearer {res.data["access"]}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        user = User.objects.get(username='test')
        self.assertTrue(user.check_password('newpassword'))

    def test_bad_password_change(self):
        res = self._register_user()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # login
        res = self.client.post('/auth/login/', data={
            'username': 'test',
            'password': '123tester123',
        })
        token = res.data["access"]

        res = self.client.post('/auth/password/change/',
                               data={
                                   'password1': 'newpassword',
                                   'password2': 'badpassword',
                               },
                               format='json',
                               HTTP_AUTHORIZATION=f'Bearer {res.data["access"]}')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(username='test')
        self.assertTrue(user.check_password('123tester123'))

    def test_token_refresh(self):
        res = self._register_user()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # login
        res = self.client.post('/auth/login/', data={
            'username': 'test',
            'password': '123tester123',
        })
        refresh = res.data["refresh"]

        res = self.client.post('/auth/token/refresh/', data={
            'refresh': refresh
        }, format='json')
        self.assertTrue(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(res.data['access'])
        self.assertTrue(res.data['refresh'])
