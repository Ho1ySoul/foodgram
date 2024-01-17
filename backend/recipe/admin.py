from django.contrib import admin

from .models import Recipe, Ingredient, MeasurementUnit, \
    RecipeIngredientRelation, ShoppingList, UserFavoriteRecipe, Tag


@admin.register(MeasurementUnit)
class MeasurementUnitAdminPanel(admin.ModelAdmin):
    fields = ['title', ]


@admin.register(Ingredient)
class IngredientAdminPanel(admin.ModelAdmin):
    fields = ['name', 'measurement_unit', ]


@admin.register(Recipe)
class RecipeAdminPanel(admin.ModelAdmin):
    fields = ['author', 'name', 'image', 'text', 'tags',
              'cooking_time']


@admin.register(Tag)
class TagAdminPanel(admin.ModelAdmin):
    fields = ['name', 'color', 'slug']


@admin.register(RecipeIngredientRelation)
class RecipeIngredientRelationAdminPanel(admin.ModelAdmin):
    fields = ['recipe', 'ingredient', 'amount']


@admin.register(ShoppingList)
class ShoppingListAdminPanel(admin.ModelAdmin):
    fields = ['user', 'recipe']


@admin.register(UserFavoriteRecipe)
class FavoriteRecipeAdminPanel(admin.ModelAdmin):
    fields = ['user', 'recipe']
