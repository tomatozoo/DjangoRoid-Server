from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from rest_framework import authentication

from comment.models import Comment
from comment import paginations, permissions
from comment.serializers import CommentListSerializer

from note.models import Note


class CommentListView(generics.ListAPIView):
    def get_queryset(self):
        note_id = self.kwargs['notePk']
        note = get_object_or_404(Note, id=note_id)
        comments = Comment.objects.filter(note=note)
        return comments
    
    serializer_class = CommentListSerializer
    
    
class CommentCreateView(generics.ListCreateAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [permissions.PublicOrIsCommmentCreator]
    authentication_classes = [authentication.TokenAuthentication]


class CommentDetailView(generics.RetrieveDestroyAPIView):
    def get_object(self):
        comment_id = self.kwargs['commentPk']
        comment = get_object_or_404(Comment, id=comment_id)
        return comment
    
    permission_classes = [permissions.IsCommmentCreator]
    authentication_classes = [authentication.TokenAuthentication]
