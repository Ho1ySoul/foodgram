from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from recipe.seriazliers import TagSerializer, MeasurementUnitSerializer, \
    IngredientSerializer, RecipeSerializer, RecipeFavoriteSerializer, \
    RecipeSerializerForPost
from recipe.models import Tag, MeasurementUnit, Ingredient, Recipe, \
    UserFavoriteRecipe, RecipeIngredientRelation


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

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return RecipeSerializerForPost
        else:
            return RecipeSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return (
                self.queryset
                .with_is_favorited(self.request.user)
                .with_is_in_shopping_cart(self.request.user)
            )

    def perform_create(self, serializer):
        print('Tyt', self.request.data)
        a = serializer.save(author=self.request.user)
        print('TYT', self.request.POST)
        # for ingredient in self.request.data['ingredients']:
        #     RecipeIngredientRelation.objects.create(
        #         recipe=Recipe.objects.get(pk=a.id),
        #         ingredient=Ingredient.objects.get(pk=ingredient['id']),
        #         amount=ingredient['amount'])


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
