from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Note(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=100, null=False)
    comment = models.CharField(max_length=1000, null=False)
    lat = models.CharField(max_length=30, null=False)
    lng = models.CharField(max_length=30, null=False)
