from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404

from .models import Post, Comment, PostReport
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
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_object(self):
        """
        Select Post by extracting uuid from url and check object permissions.
        """
        obj = get_object_or_404(Post, uuid=self.kwargs.get('uuid'))
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        return serializer.save(edited=True)
