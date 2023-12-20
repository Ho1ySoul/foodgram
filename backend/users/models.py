from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()


class UserSubscribe(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='user')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='author')
