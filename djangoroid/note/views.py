from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from rest_framework import authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from note.serializers import NoteListSerializer, NoteDetailSerializer
from note.paginations import NoteListPagination
from note.permissions import IsNoteCreator, PublicOrIsNoteCreator
from note.models import Note

from tag.models import Tag
from tag.serializers import TagSerializer

from comment.models import Comment

def get_user(request):
    token = request.META["HTTP_AUTHORIZATION"].split()[1]
    user = Token.objects.get(key=token).user
    return user

@api_view(['POST'])
def fork(request, *args, **kwargs):
    if request.method == 'POST':
        user = get_user(request)
        user_id = kwargs['userPk']
        note_id = kwargs['notePk']
        note = get_object_or_404(Note, created_by=user_id, id=note_id)
        note.fork_count += 1
        new_note = Note.objects.create(title=note.title,
                                       description=note.description,
                                       created_by=user.id,
                                       is_public=note.is_public,
                                       history=user_id)                                      
        new_note.save()
        return Response(data={'detail': 'fork'}, 
                        status=status.HTTP_201_CREATED)


class NoteListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        user = get_user(self.request)
        user_id = self.kwargs['userPk']
        notes = Note.objects.filter(created_by=user_id, is_public=True)
        return notes
    
    serializer_class = NoteListSerializer
    pagination_class = NoteListPagination
    authentication_classes = [authentication.TokenAuthentication]
    
    
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        user_id = self.kwargs['userPk']
        note_id = self.kwargs['notePk']
        note = get_object_or_404(Note, created_by=user_id, id=note_id)
        return note
    
    serializer_class = NoteDetailSerializer
    permission_classes = [PublicOrIsNoteCreator]
    authentication_classes = [authentication.TokenAuthentication]




