from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['uuid', 'username', 'date_joined',
                  'is_superuser', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['uuid', 'date_joined', 'is_superuser']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, min_length=3)
    password1 = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(detail='Passwords must match')

        return super().validate(data)


class PasswordChangeSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(detail='Passwords must match')

        return super().validate(data)
