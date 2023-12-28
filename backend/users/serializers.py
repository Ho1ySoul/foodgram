from rest_framework.serializers import ModelSerializer

from recipe.models import User
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    is_subscribed = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            "is_subscribed"
        )
