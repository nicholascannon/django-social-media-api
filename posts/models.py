from django.db import models
from uuid import uuid4


class Post(models.Model):

    class Meta:
        indexes = [
            models.Index(fields=['date_created', '-pins']),
            models.Index(fields=['author_id', 'date_created'])
        ]

    uuid = models.UUIDField(default=uuid4, null=False)
    text = models.CharField(max_length=250, null=False)
    pins = models.IntegerField(default=0, null=False)  # likes
    date_created = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True, null=False)
    edited = models.BooleanField(default=False, null=False)

    author = models.ForeignKey(
        'users.User', related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return f'<Post uuid={self.uuid} author={self.author}>'

    def get_comment_count(self):
        """
        Return the number of comments on this post.
        """
        return self.comments.count()


class Comment(models.Model):

    class Meta:
        indexes = [
            models.Index(fields=['post_id', 'date_created']),
        ]

    uuid = models.UUIDField(default=uuid4, null=False)
    text = models.CharField(max_length=100, null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        'users.User', related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)
