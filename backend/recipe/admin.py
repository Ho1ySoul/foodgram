from django.contrib import admin

from .models import Recipe, Ingredient, MeasurementUnit, \
    RecipeIngredientRelation, ShoppingList, UserFavoriteRecipe, Tag


# from  import Recipe, Ingredient, MeasurementUnit, \
#     RecipeIngredientRelation, ShoppingList, UserFavoriteRecipe, Tag


@admin.register(MeasurementUnit)
class MeasurementUnitAdminPanel(admin.ModelAdmin):
    fields = ['title', ]


@admin.register(Ingredient)
class IngredientAdminPanel(admin.ModelAdmin):
    fields = ['name', 'amount', 'measurement_unit', ]


@admin.register(Recipe)
class RecipeAdminPanel(admin.ModelAdmin):
    fields = ['author', 'title', 'img', 'description', 'tags',
              'cooking_time']


@admin.register(Tag)
class TagAdminPanel(admin.ModelAdmin):
    fields = ['title', 'color_code', 'slug', 'id']


@admin.register(RecipeIngredientRelation)
class RecipeIngredientRelationAdminPanel(admin.ModelAdmin):
    fields = ['recipe', 'ingredient', 'amount']


@admin.register(ShoppingList)
class ShoppingListAdminPanel(admin.ModelAdmin):
    fields = ['user', 'recipes']


@admin.register(UserFavoriteRecipe)
class FavoriteRecipeAdminPanel(admin.ModelAdmin):
    fields = ['user', 'recipes']
