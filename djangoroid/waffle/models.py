from django.contrib.auth.models import User
from django.db import models

from note import models as note_models


class Waffle(models.Model):
    note = models.ForeignKey(note_models.Note, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "waffle"
        verbose_name_plural = "waffles"
        db_table = "waffles"
