from rest_framework import serializers
from ServidorApp.models import User
    

class userSerializer(serializers.Serializer):
    #id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    cpf = serializers.CharField(required=True)
    lat_max = serializers.FloatField(required=True)
    lat_min = serializers.FloatField(required=True)
    long_max = serializers.FloatField(required=True)
    long_min = serializers.FloatField(required=True)
    #picture = serializers.ImageField(required=True)

class initialSerializer(serializers.Serializer):
    type = serializers.IntegerField(required=True)

class mobileLogSerializer(serializers.Serializer):
    time = serializers.DateField(required=True)
    gps = serializers.CharField(required=True)
    mobile_id = serializers.IntegerField(required=True)

class autSerializer(serializers.Serializer):
    mobile_log_id_fk = serializers.IntegerField(required=True)
    time =  serializers.DateField(required=True)
    gps =  serializers.CharField(required=True)
    valid =  serializers.BooleanField(required=True)
    type_aut = serializers.CharField(required=True)
    task_id = serializers.CharField(required=True)

class timeoutSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    mobile_log_id = serializers.IntegerField(required=True)