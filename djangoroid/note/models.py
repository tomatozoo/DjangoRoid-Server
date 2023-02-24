from django.db import models

from tag.models import Tag

# from accounts.models import CustomUser as User
from django.conf import settings
User = settings.AUTH_USER_MODEL

IMAGE_DIR = "note/"


class Canvas(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Page(models.Model):
    page = models.IntegerField()
    canvas = models.ForeignKey(
        Canvas, on_delete=models.CASCADE, related_name="pages")
    background = models.ImageField(upload_to=IMAGE_DIR, null=True)


class Note(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=200, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    history = models.CharField(max_length=20, blank=True)
    fork_count = models.IntegerField(default=0)
    waffle_count = models.IntegerField(default=0)
    # image related
    canvas = models.OneToOneField(Canvas, on_delete=models.CASCADE, null=True)
    thumbnail = models.ImageField(upload_to=IMAGE_DIR, null=True)


class NoteToTag(models.Model):
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name="tag_note")
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE, related_name="note_note")


class NoteToContributor(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_note")
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE, related_name="note_note2")
