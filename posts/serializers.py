from rest_framework import serializers

from . import models
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """
    Comment Serializer
    """
    author = UserSerializer(read_only=True)
    post = serializers.SlugRelatedField(slug_field='uuid', read_only=True)

    class Meta:
        model = models.Comment
        fields = ['uuid', 'text', 'date_created', 'post', 'author']
        read_only_fields = ['date_created', 'uuid']


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer that provides an overview of the Post model. This serializer
    summarises the comments and author models.
    """
    author = serializers.ReadOnlyField(source='author.username')
    comments = serializers.IntegerField(
        source='get_comment_count', read_only=True)

    class Meta:
        model = models.Post
        fields = ['uuid', 'text', 'author', 'pins',
                  'comments', 'date_created', 'edited']
        read_only_fields = ['uuid', 'author', 'date_created', 'pins', 'edited']
