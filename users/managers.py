from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user manager class.
    """

    def create_user(self, username, password, **kwargs):
        if not username:
            raise ValueError('Username is required')

        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if not kwargs.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True')
        if not kwargs.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True')

        return self.create_user(username, password, **kwargs)
