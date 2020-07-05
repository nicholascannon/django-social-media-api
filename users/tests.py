from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
import datetime as dt

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
