from django.db import models
from django.contrib.auth.models import User


class CustomUser(User):
    nickname = models.CharField(max_length=50, default="Anonymous")   
