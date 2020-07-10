from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status as s

from .serializers import UserSerializer, PasswordChangeSerializer

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_details(request, username=None):
    """
    Return user details for logged in user.
    """
    user = UserSerializer(instance=request.user)
    return Response(user.data)


@api_view(['GET'])
def user_details(request, username):
    """
    Return user details by username.
    """
    try:
        serializer = UserSerializer(
            instance=User.objects.get(username=username))
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=s.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change user password.
    """
    data = PasswordChangeSerializer(data=request.data)
    if data.is_valid():
        request.user.set_password(data.validated_data['password'])
        request.user.save()
        return Response(status=s.HTTP_200_OK)

    return Response(data.errors, status=s.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    """
    Register new user account.
    """
    user = UserSerializer(data=request.data)
    if user.is_valid():
        user.save()
        return Response(status=s.HTTP_201_CREATED)

    return Response(user.errors, status=s.HTTP_400_BAD_REQUEST)
