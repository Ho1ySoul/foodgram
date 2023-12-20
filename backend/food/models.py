from django.db import models

from backend.users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    measurement_unit = models.CharField(max_length=55)


class Tag(models.Model):
    title = models.CharField(max_length=255, unique=True)
    hex_code = models.IntegerField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='author_recipe')
    title = models.CharField(max_length=255)
    img = models.ImageField(upload_to='Recipe', null=True, blank=True,
                            verbose_name='Изображение')
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient,
                                         related_name='ingredients')
    tags = models.ManyToManyField(Tag,related_name='tags')
    cooking_time = models.IntegerField()

