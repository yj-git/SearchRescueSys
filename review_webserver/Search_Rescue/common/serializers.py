from rest_framework import serializers


class SelectModelSerializer(serializers.Serializer):
    name = serializers.CharField()
    desc = serializers.CharField()
    val = serializers.CharField()
    id = serializers.IntegerField()
    parent = serializers.IntegerField()
    type_select = serializers.IntegerField()
