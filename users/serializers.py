from rest_framework import serializers

from .models import User


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('uuid', 'username', 'date_joined', 'is_superuser',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, min_length=3)
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(detail='Passwords must match')

        return super().validate(data)
