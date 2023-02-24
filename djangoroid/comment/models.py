from django.db import models

from note.models import Note
from accounts.models import CustomUser


class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=200, blank=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_updated = models.BooleanField(default=False)
    waffle_count = models.IntegerField(default=0)
