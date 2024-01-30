from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, UserSubscribe
from users.serializers import (UserFavoriteSerializer, UserSerializer,
                               UserSerializerForSubcribe)


class SmallPagesPagination(PageNumberPagination):
    page_size = 4


class UserFavoriteViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return User.objects.with_is_subscribe(self.request.user)

    def post(self, request, id):
        if (not request.user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        author = get_object_or_404(User, pk=id)

        try:
            UserAuthor = UserSubscribe.objects.get(user=request.user,
                                                   author=author)
        except ObjectDoesNotExist:
            UserAuthor = UserSubscribe.objects.create(user=request.user,
                                                      author=author)
        else:
            UserSubscribe.objects.get(pk=UserAuthor.pk).delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(UserAuthor.author)
        return Response(serializer.data)

    def delete(self, request, id):
        author = get_object_or_404(User, pk=id)
        UserSubscribe.objects.get(user=request.user,
                                  author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileView(ListAPIView):
    serializer_class = UserFavoriteSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return (User.objects
                .with_is_subscribe(self.request.user)
                .filter(is_subscribed=True))


class UserProfileIsSubcribedView(UserViewSet):
    serializer_class = UserSerializerForSubcribe
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return (User.objects.with_is_subscribe(self.request.user))
