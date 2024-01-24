import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from recipe.models import (Tag, MeasurementUnit, Ingredient, Recipe,
                           RecipeIngredientRelation)
from users.serializers import UserSerializer, UserSerializerForSubcribe


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class TagSerializerForPost(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id']


class MeasurementUnitSerializer(ModelSerializer):
    class Meta:
        model = MeasurementUnit
        fields = ['id', 'title']


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class IngredientSerializerForRelation(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient',
                                            read_only=True)
    name = serializers.SlugRelatedField(source='ingredient',
                                        slug_field='name',
                                        read_only=True)
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient.measurement_unit',
        slug_field='title',
        read_only=True
    )
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = RecipeIngredientRelation
        fields = ['id', 'amount', 'name', 'measurement_unit']


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            img_format, img_str = data.split(';base64,')
            ext = img_format.split('/')[-1]
            data = ContentFile(base64.b64decode(img_str), name='img.' + ext)
        return super().to_internal_value(data)


class RecipeIngredientRelationSerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        read_only=False,
        source='ingredient'
    )

    class Meta:
        model = RecipeIngredientRelation
        fields = ['amount', 'id']


class RecipeSerializerForPost(ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer(read_only=True)

    ingredients = RecipeIngredientRelationSerializer(many=True,
                                                     source='ingredient_set')

    def create(self, validate_data):
        tags = validate_data.pop('tags', None)
        ingredients = validate_data.pop('ingredient_set', None)
        recipe = Recipe.objects.create(**validate_data)
        recipe.tags.set(tags)
        RecipeIngredientRelation.objects.bulk_create(
            [RecipeIngredientRelation(recipe=recipe, **p) for p in ingredients]
        )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredient_set', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.tags.clear()
        instance.ingredient_set.clear()
        instance.tags.set(tags)
        RecipeIngredientRelation.objects.bulk_create(
            [RecipeIngredientRelation(recipe=instance, **p) for p in
             ingredients]
        )

        return instance

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text',
                  'cooking_time', ]


class RecipeSerializer(RecipeSerializerForPost):
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializerForRelation(read_only=True,
                                                  source='ingredient_set',
                                                  many=True)
    author = UserSerializerForSubcribe(read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text',
                  'cooking_time', 'is_favorited', 'is_in_shopping_cart', ]


class RecipeFavoriteSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'cooking_time', 'name', 'image']
