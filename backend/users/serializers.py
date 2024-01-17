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
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
        )


# class RecipeSerializerForUserFavorite(ModelSerializer):
#     class Meta:
#         fields = ['id', 'name', 'image', 'cooking_time']


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
    # email = serializers.EmailField(read_only=True)
    # first_name = serializers.CharField(read_only=True)
    # last_name = serializers.CharField(read_only=True)
    # username = serializers.CharField(read_only=True)
    recipes_count = serializers.SerializerMethodField(
        method_name="get_recipe_count")

    # recipes = serializers.SerializerMethodField(
    #     method_name="get_recipe")
    recipes = RecipeForSerializer(source='recipes1', many=True)

    def get_recipe_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
        # return [Recipe.objects.filter(author=user).count() for user in obj]

    # def get_recipe(self, obj):
    #     return Recipe.objects.filter(author=obj).values('name',
    #                                                     'id',
    #                                                     'cooking_time',
    #                                                     'image')
    # return [Recipe.objects.filter(author=user)
    #         .values('name',
    #                 'id',
    #                 'cooking_time',
    #                 'image') for user in obj]

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
