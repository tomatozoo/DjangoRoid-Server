from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from rest_framework import authentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import permissions

from note.serializers import NoteListSerializer, NoteDetailSerializer
from note.paginations import NoteListPagination
from note.permissions import IsNoteCreator, PublicOrIsNoteCreator
from note.models import Note, NoteToTag

from tag.models import Tag
from tag.serializers import TagSerializer

from accounts.models import User

from comment.models import Comment

def get_user(request):
    try:
        token = request.META["HTTP_AUTHORIZATION"].split()[1]
    except:
        return Response(f"invalid token", status=status.HTTP_401_UNAUTHORIZED)
    user = Token.objects.get(key=token).user
    return user

def create_tag_note_objects(tags, note):
    for tag in tags:
        NoteToTag.objects.create(tag=Tag.objects.get(name=tag), note=note)

@api_view(['POST'])
def fork(request, *args, **kwargs):
    if request.method == 'POST':
        user = get_user(request)
        if not isinstance(user, User):
            return user
        user_id = kwargs['userPk']
        note_id = kwargs['notePk']
        note = get_object_or_404(Note, created_by=user_id, id=note_id, is_public=True)
        note.fork_count += 1
        new_note = Note.objects.create(title=note.title,
                                       description=note.description,
                                       created_by=user.id,
                                       is_public=note.is_public,
                                       history=user_id)                                      
        new_note.save()
        return Response(data={'detail': 'fork'}, 
                        status=status.HTTP_201_CREATED)


class NoteListView(generics.ListAPIView):
    def get_queryset(self):
        user_id = self.kwargs['userPk']
        user = User.objects.get(id=user_id)
        notes = Note.objects.filter(created_by=user, is_public=True)
        return notes
    
    serializer_class = NoteListSerializer
    pagination_class = NoteListPagination
    

class NoteCreateView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        user = get_user(request)
        request.data['created_by'] = user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        note = serializer.save()
        if 'tags' in self.request.data:
            create_tag_note_objects(self.request.data['tags'], note)
    
    serializer_class = NoteDetailSerializer
    authentication_classes = [authentication.TokenAuthentication]
    
    
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        user_id = self.kwargs['userPk']
        note_id = self.kwargs['notePk']
        note = get_object_or_404(Note, created_by=user_id, id=note_id)
        if not self.request.method in permissions.SAFE_METHODS:
            self.check_object_permissions(self.request, note)
        return note

    serializer_class = NoteDetailSerializer
    permission_classes = [IsNoteCreator]
    authentication_classes = [authentication.TokenAuthentication]
