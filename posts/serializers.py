from rest_framework import serializers

from . import models


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='uuid', read_only=True)

    class Meta:
        model = models.Post
        fields = ['uuid', 'text', 'author', 'pins', 'date_created']
        read_only_fields = ['uuid', 'pins', 'date_created']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    post = serializers.SlugRelatedField(slug_field='uuid', read_only=True)

    class Meta:
        model = models.Comment
        fields = ['uuid', 'text', 'date_created']
        read_only_fields = ['date_created', 'uuid']


class PostReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PostReport
        fields = '__all__'  # model is for admin use only
