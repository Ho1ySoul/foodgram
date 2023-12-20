from rest_framework.serializers import ModelSerializer

from recipe.models import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color_code', 'slug']
