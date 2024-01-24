from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from recipe.views import (IngredientViewSet, MeasurementUnitViewSet,
                          RecipesFavoriteViewSet,
                          RecipesShoppingCartDownloadViewSet,
                          RecipesShoppingCartViewSet, RecipesViewSet,
                          TagViewSet)
from users.views import (UserFavoriteViewSet, UserProfileIsSubcribedView,
                         UserProfileView)

router = SimpleRouter()
router.register(r'api/tags', TagViewSet, basename='tags')
router.register(r'api/ingredients', IngredientViewSet, basename='tags')
router.register(r'api/recipes', RecipesViewSet, basename='recipes')
router.register(r'api/measurementUnit', MeasurementUnitViewSet,
                basename='measurementUnit')
router.register(r'api/users', UserProfileIsSubcribedView,
                basename='UserProfileIsSubcribedView')

urlpatterns = []
urlpatterns += [
    path('api/users/subscriptions/',
         UserProfileView.as_view()),
    path('api/recipes/download_shopping_cart/',
         RecipesShoppingCartDownloadViewSet.as_view()),
]
urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls'), name='auth'),
    path('api/recipes/<int:id>/favorite/',
         RecipesFavoriteViewSet.as_view()),
    path('api/recipes/<int:id>/shopping_cart/',
         RecipesShoppingCartViewSet.as_view()),
    path('api/users/<int:id>/subscribe/',
         UserFavoriteViewSet.as_view()),

    re_path(r'api/auth/', include('djoser.urls.authtoken')),
]
