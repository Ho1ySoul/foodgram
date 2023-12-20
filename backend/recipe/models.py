from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MeasurementUnit(models.Model):
    title = models.CharField(max_length=255)


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    measurement_unit = models.ForeignKey(MeasurementUnit,
                                         on_delete=models.CASCADE,
                                         related_name='Ingredient')


class Tag(models.Model):
    title = models.CharField(max_length=255, unique=True)
    color_code = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipe')

    title = models.CharField(max_length=255)
    img = models.ImageField(upload_to='Recipe',
                            null=True,
                            blank=True,
                            verbose_name='Изображение')
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient,
                                         through="RecipeIngredientRelation",
                                         related_name='ingredients')
    tags = models.ManyToManyField(Tag, related_name='tags')
    cooking_time = models.PositiveIntegerField()


class RecipeIngredientRelation(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField("Кол-во ингридиентов")


class ShoppingList(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='recipe2')
    recipes = models.ManyToManyField(Recipe, related_name='recipes2')


class UserFavoriteRecipe(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='user1')
    recipes = models.ManyToManyField(Recipe, related_name='recipes1')
