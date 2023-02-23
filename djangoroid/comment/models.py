from django.contrib.auth.models import User
from django.db import models

from note import models as note_models


class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    note = models.ForeignKey(note_models.Note, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)
    waffle_count = models.IntegerField()

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        db_table = "comments"
