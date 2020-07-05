from django.contrib import admin

from . import models

admin.register(models.Post)
admin.register(models.Comment)
admin.register(models.PostReport)
