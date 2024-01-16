"""
URL configuration for foodgram project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import SimpleRouter

from recipe.views import (TagViewSet, MeasurementUnitViewSet,
                          IngredientViewSet,
                          RecipesViewSet, RecipesFavoriteViewSet,
                          RecipesShoppingCartViewSet,
                          RecipesShoppingCartDownloadViewSet)

from recipe import views
from users.views import UserFavoriteViewSet, UserProfileView

router = SimpleRouter()
router.register(r'api/tags', TagViewSet, basename='tags')
router.register(r'api/ingredients', IngredientViewSet, basename='tags')
router.register(r'api/recipes', RecipesViewSet, basename='recipes')
router.register(r'api/measurementUnit', MeasurementUnitViewSet,
                basename='measurementUnit')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/subscriptions/',
         UserProfileView.as_view()),
    path('api/', include('djoser.urls'), name='auth'),
    path('api/recipes/<int:id>/favorite/',
         RecipesFavoriteViewSet.as_view()),
    path('api/recipes/<int:id>/shopping_cart/',
         RecipesShoppingCartViewSet.as_view()),
    path('api/users/<int:id>/subscribe/',
         UserFavoriteViewSet.as_view()),
    path('api/recipes/download_shopping_cart/',
         RecipesShoppingCartDownloadViewSet.as_view()),
    re_path(r'api/auth/', include('djoser.urls.authtoken')),
    # path('api/users/<int:id>/',
    #      UserProfileView.as_view()),
]
urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
