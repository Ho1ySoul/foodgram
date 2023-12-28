import base64

from django.core.files.base import ContentFile
from requests.compat import basestring
from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from recipe.models import Tag, MeasurementUnit, Ingredient, Recipe, \
    RecipeIngredientRelation
from rest_framework import serializers

from users.serializers import UserSerializer


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class MeasurementUnitSerializer(ModelSerializer):
    class Meta:
        model = MeasurementUnit
        fields = ['id', 'title']


class IngredientSerializer(ModelSerializer):
    measurement_unit = serializers.SlugRelatedField(slug_field="title",
                                                    read_only=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


# class Base64ImageField(serializers.ImageField):
#     def from_native(self, data):
#         if isinstance(data, basestring) and data.startswith('data:image'):
#             # base64 encoded image - decode
#             format, imgstr = data.split(';base64,')  # format ~= data:image/X,
#             ext = format.split('/')[-1]  # guess file extension
#
#             data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
#
#         return super(Base64ImageField, self).from_native(data)
class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            img_format, img_str = data.split(';base64,')
            ext = img_format.split('/')[-1]
            data = ContentFile(base64.b64decode(img_str), name='img.' + ext)
        return super().to_internal_value(data)


class RecipeSerializerForPost(ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer(read_only=True)

    ingredients = serializers.SerializerMethodField(
        method_name="get_ingredients")

    def get_ingredients(self, obj):
        my_list = list()
        all_ingredients = obj.ingredients.through.objects.filter(
            recipe__name=obj.name)
        for ingredient_to_recipe in all_ingredients:
            my_dict = dict()
            my_dict['id'] = ingredient_to_recipe.id
            my_dict['amount'] = ingredient_to_recipe.amount
            my_dict['measurement_unit'] = (ingredient_to_recipe
                                           .ingredient
                                           .measurement_unit
                                           .title)
            my_dict['name'] = ingredient_to_recipe.ingredient.name

            my_list.append(my_dict)
        return my_list

    # def create(self, validated_data):
    #     return RecipeIngredientRelation.objects.create(recipe=validated_data,ingredients=)

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text',
                  'cooking_time']


class RecipeSerializer(RecipeSerializerForPost):
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text',
                  'cooking_time', 'is_favorited', 'is_in_shopping_cart',
                  ]


class RecipeFavoriteSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'cooking_time', 'name', 'image']
