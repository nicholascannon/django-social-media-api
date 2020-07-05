from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status as s

from .serializers import UserSerializer, UserRegisterSerializer, UserDetailsSerializer

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    """
    Return user details for logged in user.
    """
    user = UserDetailsSerializer(instance=request.user)
    return Response(user.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change user password.
    """
    if request.data.get('password1') and request.data.get('password2'):
        if request.data.get('password1') == request.data.get('password2'):
            request.user.set_password(request.data['password1'])
            request.user.save()

            return Response(status=s.HTTP_200_OK)

    return Response({'err': 'Passwords must match'}, status=s.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    """
    Register new user account.
    """
    data = UserRegisterSerializer(data=request.data)
    if data.is_valid():
        user = UserSerializer(data={
            'username': data.validated_data['username'],
            'password': data.validated_data['password1'],
        })
        if user.is_valid():
            user.save()
            return Response(status=s.HTTP_201_CREATED)

        return Response(user.error_messages, status=s.HTTP_400_BAD_REQUEST)

    return Response(data.error_messages, status=s.HTTP_400_BAD_REQUEST)
