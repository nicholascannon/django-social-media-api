from rest_framework import serializers

from . import models
from users.serializers import UserDetailsSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserDetailsSerializer(read_only=True)
    post = serializers.SlugRelatedField(slug_field='uuid', read_only=True)

    class Meta:
        model = models.Comment
        fields = ['uuid', 'text', 'date_created', 'post', 'author']
        read_only_fields = ['date_created', 'uuid']


class PostSerializer(serializers.ModelSerializer):
    author = UserDetailsSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = models.Post
        fields = ['uuid', 'text', 'author', 'comments', 'pins', 'date_created']
        read_only_fields = ['uuid', 'pins', 'date_created']


class PostReportSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    user = UserDetailsSerializer()

    class Meta:
        model = models.PostReport
        fields = '__all__'  # model is for admin use only
