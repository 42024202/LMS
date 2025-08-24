from rest_framework import serializers
from .models import MyUser, Email2FACode


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'avatar', 'role', 'is_active', 'is_staff']


class Email2FACodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email2FACode
        fields = ['id', 'user', 'code', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = MyUser(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
