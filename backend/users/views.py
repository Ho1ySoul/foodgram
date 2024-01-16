from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import UserSubscribe, User
from users.serializers import UserSerializer, UserFavoriteSerializer


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

        serializer = UserFavoriteSerializer(UserAuthor.author)
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


class UserProfileView(GenericAPIView):

    def get_queryset(self):
        return User.objects.all()

    # def get_object(self, id):
    #     queryset = self.get_queryset()
    #     user = queryset.filter(pk=id)
    #     return user
    def get(self, request):
        user_subscribe = UserSubscribe.objects.filter(user=request.user, )
        authors = user_subscribe.values('author')
        serializer = UserSerializer(authors)
        return Response(serializer.data)
