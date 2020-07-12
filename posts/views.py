from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as s
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly


class PostListCreateAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return all posts for logged in user.
        """
        return Post.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    lookup_field = 'uuid'

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        return serializer.save(edited=True)


class PinPostView(APIView):
    """
    Allows any authenticated user to pin (like) a post. Currently a user can 
    pin the same post as many times as they like.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, uuid):
        """
        Increment post pins by 1.
        """
        post = get_object_or_404(Post, uuid=uuid)
        post.pins += 1
        post.save()
        return Response(status=s.HTTP_200_OK)
