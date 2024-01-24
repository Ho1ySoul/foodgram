from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Exists, OuterRef

User = get_user_model()


class RecipeQuerySet(models.QuerySet):
    def with_is_favorited(self, user):
        return self.annotate(
            is_favorited=(
                Exists(UserFavoriteRecipe.objects.filter(
                    user=user,
                    recipe=OuterRef("pk"))
                )

            )
        )

    def with_is_in_shopping_cart(self, user):
        return self.annotate(
            is_in_shopping_cart=(
                Exists(ShoppingList.objects.filter(user=user,
                                                   recipe=OuterRef("pk"))))
        )


class MeasurementUnit(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title}'


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    measurement_unit = models.ForeignKey(MeasurementUnit,
                                         on_delete=models.CASCADE,
                                         related_name='ingredient')

    def __str__(self):
        return f'{self.name}: {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    color = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name} : {self.slug}'


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='author_recipes')

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Recipe',
                              null=True,
                              blank=True,
                              verbose_name='Изображение')
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient,
                                         through="RecipeIngredientRelation",
                                         related_name='ingredients_in_recipe')
    tags = models.ManyToManyField(Tag, related_name='tags_in_recipe')
    cooking_time = models.PositiveIntegerField()

    objects = RecipeQuerySet.as_manager()

    def __str__(self):
        return f'{self.name} : {self.author}'


class RecipeIngredientRelation(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               null=True,
                               related_name='ingredient_set')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   null=True,
                                   related_name='recipe_set')
    amount = models.PositiveIntegerField("Кол-во ингридиентов")


class ShoppingList(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='recipes_in_shopping_list')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='+')


class UserFavoriteRecipe(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='+')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipes_in_favorite')
