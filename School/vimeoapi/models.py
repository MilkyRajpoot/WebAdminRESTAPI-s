from django.db import models
import json
import jsonfield

# Create your models here.

class Vimeo(models.Model):
    title = models.CharField(max_length=100)
    college = models.CharField(max_length=10)
    sub = models.CharField(max_length=10)
    data = jsonfield.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class VimeoStatus(models.Model):
    status = models.BooleanField(default=False)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)