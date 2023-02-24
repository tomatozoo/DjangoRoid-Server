from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from rest_framework import authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response

from note.models import Note
from note.serializers import NoteListSerializer, NoteDetailSerializer
from note.paginations import NoteListPagination
from note.permissions import IsNoteCreator, PublicOrIsNoteCreator

from tag.models import Tag
from tag.serializers import TagSerializer

# from comment.models import Comment

@api_view(['POST'])
def fork(request, *args, **kwargs):
    if request.method == 'POST':
        user_id = kwargs['userPk']
        note_id = kwargs['notePk']
        note = get_object_or_404(Note, created_by=user_id, id=note_id)
        note['fork_count'] += 1
        fork_keys = ['title', 'description', 'is_public', 'tag', 'waffle_count', 'contributor']
        origin = {k:note[k] for k in fork_keys}
        new_note = Note.objects.create(created_by=user_id,
                                       history=note['created_by'],
                                       **origin)
        new_note.save()
        return Response(data={'detail' : 'fork'})


class NoteListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        user_id = self.kwargs['userPk']
        print(user_id)
        notes = Note.objects.filter(created_by=user_id)
        return notes
    
    serializer_class = NoteListSerializer
    pagination_class = NoteListPagination
    
    
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        user_id = self.kwargs['userPk']
        note_id = self.kwargs['notePk']
        note = get_object_or_404(Note, created_by=user_id, id=note_id)
        return note
    
    serializer_class = NoteDetailSerializer
    permission_classes = [PublicOrIsNoteCreator]
    authentication_classes = [authentication.TokenAuthentication]




