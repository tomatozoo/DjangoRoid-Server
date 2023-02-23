from django.db import models
from django.contrib.auth.models import User
from tag.models import Tag


class CustomUser(User):
    nickname = models.CharField(max_length=50, blank=False)   


class UserToTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    
    