from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveDestroyAPIView
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as s
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostListCreateAPIView(ListCreateAPIView):
    """
    Lists the currently logged in users posts with a GET and allows a user to 
    create a new post with POST. Must be logged in to access this route.

    EXAMPLE:
        GET -> /posts/ -> return a list of posts
        POST -> /posts/ -> create new post
    """
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
    """
    Selects post by UUID and displays it's details. Anon users able to read post
    details with GET. Must be authenticated and be the owner of the post to make 
    PUT and DELETE requests.

    EXAMPLE:
        GET -> /posts/<uuid>/ -> return post details
        PUT -> /posts/<uuid>/ -> make an edit to the post text (if owner)
        DELETE -> /posts/<uuid>/ -> delete post (if owner)
    """
    queryset = Post.objects.all()
    lookup_field = 'uuid'

    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        return serializer.save(edited=True)


class PinPostAPIView(APIView):
    """
    Allows any authenticated user to pin (like) a post. This endpoint increments
    a posts pins by 1.

    NOTE:   Currently a user can pin the same post as many times as they like. 
            This could be avoided by pulling the pins out into their own table 
            with one to one FK to a post and user, would require a check before
            pinning post (some indexing on the table would be a good idea too).

    EXAMPLE:
        PUT -> /posts/<uuid>/pin/ -> increment post pins by 1
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


class CommentListCreateAPIView(ListCreateAPIView):
    """
    Lists all the comments for a given post. Anon users can read comments. Must
    be logged in to create comments on the post.

    EXAMPLE:
        GET -> /posts/<uuid>/comments/ -> returns all comments for post with uuid
        POST -> /posts/<uuid>/comments/ -> create new comment on post with uuid
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.order_by('-date_created').filter(
            post__uuid=self.kwargs['uuid'])

    def perform_create(self, serializer):
        post = Post.objects.get(uuid=self.kwargs['uuid'])
        return serializer.save(author=self.request.user, post=post)


class CommentRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    """
    Allows user to delete their comment on a post. UUID for the post and comment
    required. Users can only delete their own comments. Also enable the retrieval
    of a single comments details.

    EXAMPLE:
        GET -> /posts/<post_uuid>/comments/<comment_uuid>/ -> comment details
        DELETE -> /posts/<post_uuid>/comments/<comment_uuid>/ -> delete comment
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_object(self):
        comment = get_object_or_404(Comment, uuid=self.kwargs['comment_uuid'],
                                    post__uuid=self.kwargs['post_uuid'])
        self.check_object_permissions(self.request, comment)
        return comment
