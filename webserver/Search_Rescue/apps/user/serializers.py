from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    is_active = serializers.BooleanField()
