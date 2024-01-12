from django.shortcuts import render
from rest_framework.views import APIView

from users.models import UserSubscribe, User


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

        return UserAuthor
