from django.db import models

# from accounts.models import CustomUser as User
from django.contrib.auth import get_user_model  
User = get_user_model()

from note.models import Note
from comment.models import Comment

class Waffle(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class NoteWaffle(Waffle):
    obj = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="note")


class CommentWaffle(Waffle):
    obj = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment")
