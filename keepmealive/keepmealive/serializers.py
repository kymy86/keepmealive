from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False, default="")
    last_name = serializers.CharField(required=False, default="")
    is_staff = serializers.BooleanField(default=True)
    is_active = serializers.BooleanField(default=True)
    is_superuser = serializers.BooleanField(default=False)
    last_login = serializers.DateTimeField(required=False)
    class Meta:
        model = User
        fields = ('is_staff', 'username', 'email', 'first_name', 'last_name', 'last_login')

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    hash = serializers.UUIDField(required=True)
    password = serializers.CharField(required=True)





