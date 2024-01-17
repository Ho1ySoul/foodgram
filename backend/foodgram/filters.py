from django_filters.rest_framework import FilterSet
from django_filters import rest_framework as filters

from recipe.models import Recipe


class CategoriesFilter(FilterSet):
    is_favorited = filters.CharFilter(field_name='is_favorited',
                                      label='Фильтрация по избранному')

    tags = filters.CharFilter(field_name='tags', lookup_expr='slug')
    author = filters.CharFilter(field_name='author')

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'tags', 'author']
