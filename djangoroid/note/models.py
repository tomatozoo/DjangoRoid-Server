from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    history = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    contributor = models.ManyToManyField("User", through="NoteContributor")
    fork_count = models.IntegerField(default=0)
    waffle_count = models.IntegerField(default=0)
    tags = models.ManyToManyField("Tag", through="TagToNote")
    # file

    class Meta:
        verbose_name = "note"
        verbose_name_plural = "notes"
        db_table = "notes"

    def __str__(self):
        return str(self.title)


class NoteContributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=30)


class TagToNote(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
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


class Waffle(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "waffle"
        verbose_name_plural = "waffles"
        db_table = "waffles"
