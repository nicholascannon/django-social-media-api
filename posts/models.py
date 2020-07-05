from django.db import models
from uuid import uuid4


class Post(models.Model):

    class Meta:
        indexes = [
            models.Index(fields=['date_created', '-pins']),
        ]

    uuid = models.UUIDField(default=uuid4, null=False, blank=True)
    text = models.CharField(max_length=250, null=False)
    pins = models.IntegerField(default=0, null=False, blank=True)  # likes
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    visible = models.BooleanField(default=True, null=False, blank=True)

    author = models.ForeignKey(
        'users.User', related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return f'<Post uuid={self.uuid} author={self.author}>'


class Comment(models.Model):

    class Meta:
        indexes = [
            models.Index(fields=['post_id', 'date_created']),
        ]

    uuid = models.UUIDField(default=uuid4, null=False, blank=True)
    text = models.CharField(max_length=100, null=False)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)

    author = models.ForeignKey(
        'users.User', related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)


class PostReport(models.Model):
    uuid = models.UUIDField(default=uuid4, null=False, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)

    post = models.ForeignKey(
        'Post', related_name='reports', on_delete=models.CASCADE)
    user = models.ForeignKey(
        'users.User', related_name='reports', on_delete=models.CASCADE)
