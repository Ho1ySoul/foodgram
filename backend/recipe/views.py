from django.db.models import Sum
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.db.models import F

from foodgram.filters import CategoriesFilter
from recipe.seriazliers import (TagSerializer, MeasurementUnitSerializer,
                                IngredientSerializer, RecipeSerializer,
                                RecipeFavoriteSerializer,
                                RecipeSerializerForPost)
from recipe.models import (Tag, MeasurementUnit, Ingredient, Recipe,
                           UserFavoriteRecipe, RecipeIngredientRelation,
                           ShoppingList)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None


class MeasurementUnitViewSet(ModelViewSet):
    queryset = MeasurementUnit.objects.all()
    serializer_class = MeasurementUnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None


class RecipesViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filterset_class = CategoriesFilter

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return RecipeSerializerForPost
        else:
            return RecipeSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return (
                self.queryset
                .prefetch_related('tags','ingredients')
                .select_related('author')
                .with_is_favorited(self.request.user)
                .with_is_in_shopping_cart(self.request.user))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipesFavoriteViewSet(APIView):
    def post(self, request, id):
        recipe = Recipe.objects.filter(id=id).first()

        if not recipe:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if UserFavoriteRecipe.objects.filter(user=request.user,
                                             recipe=recipe):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        new_favorite_recipe = UserFavoriteRecipe.objects.create(
            user=request.user,
            recipe=recipe)
        new_favorite_recipe.save()
        serializer = RecipeFavoriteSerializer(recipe)
        return Response(serializer.data)

    def delete(self, request, id):
        recipe = Recipe.objects.get(id=id)
        UserFavoriteRecipe.objects.filter(user=request.user,
                                          recipe=recipe).delete()
        return Response({"message": "Рецепт успешно удалён"})


class RecipesShoppingCartViewSet(APIView):
    def post(self, request, id):
        recipe = Recipe.objects.filter(id=id).first()
        HaveShoppingList = ShoppingList.objects.filter(user=request.user,
                                                       recipe=recipe)
        if (HaveShoppingList):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = RecipeFavoriteSerializer(recipe)
        ShoppingList.objects.create(user=request.user, recipe=recipe)

        return Response(serializer.data)

    def delete(self, request, id):
        recipe = Recipe.objects.get(id=id)
        ShoppingList.objects.filter(user=request.user,
                                    recipe=recipe).delete()
        return Response({"message": "Рецепт успешно удалён"})


class RecipesShoppingCartDownloadViewSet(APIView):

    def get(self, request):
        shop_recipes = ShoppingList.objects.filter(
            user=self.request.user).values('recipe')
        ingredients = (
            RecipeIngredientRelation
            .objects
            .filter(recipe__in=shop_recipes)
            .values('ingredient')
            .annotate(
                amount_ingredient=Sum('amount'),
                ingredient_name=F('ingredient__name'),
                ingredient_measurement_unit=F(
                    'ingredient__measurement_unit__title'),

            )
        )

        print(ingredients)
        ingredients_line = ''
        for ingredient in ingredients:
            ingredients_line += (f'{ingredient['ingredient_name']} :'
                                 f'  {ingredient['amount_ingredient']} '
                                 f'{ingredient['ingredient_measurement_unit']}\n')

        return HttpResponse(
            ingredients_line,
            headers={'Content-Type': 'text/plain'}
        )
