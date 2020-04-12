from rest_framework import serializers


class SelectModelSerializer(serializers.Serializer):
    name = serializers.CharField()
    desc = serializers.CharField()
    val = serializers.CharField()
    id = serializers.IntegerField()
    parent = serializers.IntegerField()
    type_select = serializers.IntegerField()
    # TODO:[-] + 20-04-12 新补充了一部分
    menu_title = serializers.CharField()  # 菜单 title
    menu_content = serializers.CharField()  # 菜单content
    menu_level = serializers.IntegerField()  # 菜单等级
    menu_url = serializers.CharField()  # 菜单url(跳转路径)
    menu_sort = serializers.IntegerField()  # 菜单排序
    menu_class = serializers.CharField()  # 菜单样式
