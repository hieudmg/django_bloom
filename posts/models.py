from django.db import models
from django.conf import settings


class Posts(models.Model):
    title = models.CharField(max_length=1000)
    created_at = models.TimeField(auto_now_add=True)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey('Categories', models.SET_NULL, blank=True, null=True)


class Categories(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
