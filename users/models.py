from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

from .managers import UserManager


class User(AbstractUser):
    """
    Custom user model
    """
    email = None
    first_name = None
    last_name = None
    uuid = models.UUIDField(default=uuid4)

    objects = UserManager()

    def __str__(self):
        return self.username
