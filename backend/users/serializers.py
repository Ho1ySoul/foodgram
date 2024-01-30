from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from recipe.models import User, Recipe


class RecipeForSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('name',
                  'id',
                  'image',
                  'cooking_time')


class UserSerializerForSubcribe(ModelSerializer):
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class UserSerializer(ModelSerializer):
    is_subscribed = serializers.BooleanField(read_only=True)
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipe_count')
    recipes = RecipeForSerializer(source='author_recipes', many=True)

    def get_recipe_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'recipes_count',
            'recipes',
            'is_subscribed',
        )


class UserFavoriteSerializer(ModelSerializer):
    is_subscribed = serializers.BooleanField(required=False)
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipe_count')
    recipes = RecipeForSerializer(source='author_recipes', many=True)

    def get_recipe_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'recipes_count',
            'recipes',
            'is_subscribed',
        )
