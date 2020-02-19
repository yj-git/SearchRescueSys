from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    is_active = serializers.BooleanField()


class CaseSerializer(serializers.Serializer):
    # 根目录
    root_path = serializers.CharField()
    # 创建的case目录
    case_path = serializers.CharField()
    # case创建时间
    create_date = serializers.DateTimeField()
    # 预报的时间
    forecast_date = serializers.DateTimeField()
    # 保存case的部分提交的参数
    case_name = serializers.CharField()
    case_desc = serializers.CharField()
    # case 的code
    case_code = serializers.CharField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    wind_coefficient = serializers.FloatField()
    wind_dir = serializers.FloatField()
    simulation_step = serializers.FloatField()
    simulation_duration=serializers.FloatField()
    console_step = serializers.FloatField()
    current_nondeterminacy = serializers.FloatField()
    equation = serializers.IntegerField()
    radius = serializers.FloatField()
    nums = serializers.IntegerField()
    area = serializers.IntegerField()


class JobMidSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    name = serializers.CharField()
    state = serializers.IntegerField()
    area = serializers.IntegerField()
    tag = serializers.CharField()
    rate = serializers.IntegerField()
    code = serializers.CharField()


class CaseNumsMidSerializer(serializers.Serializer):
    date = serializers.DateField()
    nums = serializers.IntegerField()
