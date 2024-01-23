import base64
import trace

from django.core.files.base import ContentFile
from rest_framework.serializers import ModelSerializer

from recipe.models import User, Recipe
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            img_format, img_str = data.split(';base64,')
            ext = img_format.split('/')[-1]
            data = ContentFile(base64.b64decode(img_str), name='img.' + ext)
        return super().to_internal_value(data)


class RecipeForSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('name',
                  'id',
                  'image',
                  'cooking_time')


# class RecipeSerializerUser(ModelSerializer):
#     recipe = RecipeForSerializer(source='recipes',
#                                  many=True, read_only=True)
#
#     class Meta:
#         model = User
#         fields = ['recipe']


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


# class RecipeSerializerForUserFavorite(ModelSerializer):
#     class Meta:
#         fields = ['id', 'name', 'image', 'cooking_time']


class UserSerializer(ModelSerializer):
    is_subscribed = serializers.BooleanField(read_only=True)
    recipes_count = serializers.SerializerMethodField(
        method_name="get_recipe_count")
    # recipes_count = serializers.IntegerField(read_only=True)
    recipes = RecipeForSerializer(source='recipes1', many=True)

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
        method_name="get_recipe_count")
    recipes = RecipeForSerializer(source='recipes1', many=True)

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
