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
