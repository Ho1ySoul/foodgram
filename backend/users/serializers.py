from rest_framework.serializers import ModelSerializer

from recipe.models import User, Recipe
from rest_framework import serializers


class RecipeSerializerForUserFavorite(ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'image', 'cooking_time']


class UserSerializer(ModelSerializer):
    is_subscribed = serializers.BooleanField(read_only=True, default=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    recipes_count = serializers.SerializerMethodField(
        method_name="get_recipe_count")

    recipes = serializers.SerializerMethodField(
        method_name="get_recipe")

    def get_recipe_count(self, obj):
        print('tyt user na list', obj)
        return Recipe.objects.filter(author=obj).count()

    def get_recipe(self, obj):
        return Recipe.objects.filter(author=obj).values('name',
                                                        'id',
                                                        'cooking_time',
                                                        'image')

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes_count',
            'recipes'
        )


class UserFavoriteSerializer(ModelSerializer):
    is_subscribed = serializers.BooleanField(read_only=True, default=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    recipes_count = serializers.SerializerMethodField(
        method_name="get_recipe_count")

    recipes = serializers.SerializerMethodField(
        method_name="get_recipe")

    def get_recipe_count(self, obj):
        return Recipe.objects.filter(author_id=obj.pk).count()

    def get_recipe(self, obj):
        return Recipe.objects.filter(author_id=obj.pk).values('name',
                                                              'id',
                                                              'cooking_time',
                                                              'image')

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes_count',
            'recipes'
        )
