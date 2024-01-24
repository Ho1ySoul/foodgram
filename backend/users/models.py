from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Exists, OuterRef


class UserCustomManager(UserManager):
    def with_is_subscribe(self, user):
        user_subsribed = UserSubscribe.objects.filter(user=user,
                                                      author=OuterRef('pk'))
        return self.annotate(is_subscribed=(Exists(user_subsribed)))


class User(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True)

    objects = UserCustomManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class UserSubscribe(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='user')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='author')
