from rest_framework import serializers

from . import models


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField()
    comments = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = models.Post
        fields = ('uuid', 'text', 'pins', 'date_created',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = models.Comment
        fields = ('uuid', 'text', 'date_created',)


class PostReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PostReport
        fields = '__all__'  # model is for admin use only
