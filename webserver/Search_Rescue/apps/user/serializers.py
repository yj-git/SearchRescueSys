from rest_framework import serializers
from .models import *


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    is_active = serializers.BooleanField()
