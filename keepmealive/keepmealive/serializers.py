from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    hash = serializers.UUIDField(required=True)
    password = serializers.CharField(required=True)





