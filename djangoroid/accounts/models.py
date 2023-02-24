from django.db import models
from django.contrib.auth.models import AbstractUser
from tag.models import Tag

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=False)   
    # username = models.CharField(max_length=20, blank=False)
    password = models.CharField(max_length=20, blank=False)

class UserToTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    