from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import UserSubscribe, User
from users.serializers import UserSerializer


# Create your views here.
class UserFavoriteViewSet(APIView):
    def post(self, request, id):
        try:
            UserAuthor = UserSubscribe.objects.get(user=request.user,
                                                   author=User.objects.get(
                                                       pk=id))
        except:
            UserAuthor = UserSubscribe.objects.create(user=request.user,
                                                      author=User.objects.get(
                                                          pk=id))

        return Response(UserAuthor)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        user = User.objects.get(pk=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
