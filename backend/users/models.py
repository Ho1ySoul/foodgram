from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Exists, OuterRef, Count


# from recipe.models import Recipe


class UserQuerySet(models.QuerySet):
    def with_is_subscribe(self, user):
        return self.annotate(
            is_subscribed=(
                Exists(UserSubscribe.objects.filter(user=user,
                                                    author=OuterRef(
                                                        "pk")))
            )
        )

    # def with_recipe_count(self, user):
    #     return self.annotate(
    #         recipes_count=Count(Recipe.objects.filter(author=user)))
    #


class User(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True)

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
