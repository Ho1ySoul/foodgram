import http.client

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import UserSubscribe, User
from users.serializers import UserSerializer, UserFavoriteSerializer, \
    UserSerializerForSubcribe


class SmallPagesPagination(PageNumberPagination):
    page_size = 4


class UserFavoriteViewSet(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, id):
        if (not request.user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        author = get_object_or_404(User, pk=id)

        try:
            UserAuthor = UserSubscribe.objects.get(user=request.user,
                                                   author=author)
        except:
            UserAuthor = UserSubscribe.objects.create(user=request.user,
                                                      author=author)
        else:
            UserSubscribe.objects.get(pk=UserAuthor.pk).delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(UserAuthor.author)
        print('mydata', serializer.data)
        serializer.data['is_subscribed'] = True
        return Response(serializer.data)

    def delete(self, request, id):
        author = get_object_or_404(User, pk=id)
        UserSubscribe.objects.get(user=request.user,
                                  author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def get(self, request):
    #     serializer = UserFavoriteSerializer(
    #         UserSubscribe.objects.filter(user=request.user).values('author'))
    #     return Response(serializer.data)


class UserProfileView(ListAPIView):
    pagination_class = SmallPagesPagination

    def get_queryset(self):
        return User.objects.all()

    # def get_object(self, id):
    #     queryset = self.get_queryset()
    #     user = queryset.filter(pk=id)
    #     return user
    def get(self, request, *args, **kwargs):
        user_subscribe = UserSubscribe.objects.filter(user=request.user)

        authors = user_subscribe.values('author')
        users = [User.objects.get(pk=user['author']) for user in authors]
        serializer = UserFavoriteSerializer(users, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)
        # return serializer.data
