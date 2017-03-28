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

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'password', 'is_active')
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.password = validated_data.get('password', instance.password)
        instance.set_password(instance.password)
        instance.save()
        return instance



class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'last_login')


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    hash = serializers.UUIDField(required=True)
    password = serializers.CharField(required=True)





