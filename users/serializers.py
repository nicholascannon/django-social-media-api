from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['uuid', 'username', 'date_joined',
                  'password', 'confirm_password']
        read_only_fields = ['uuid', 'date_joined']

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError('Passwords must match')

        del data['confirm_password']
        data['password'] = make_password(data['password'])
        return data


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(detail='Passwords must match')

        return data
