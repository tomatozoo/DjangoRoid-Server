from django.shortcuts import render, get_object_or_404

from rest_framework import permissions as rest_permissions
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from comment.models import Comment
from comment import paginations, permissions
from comment.serializers import CommentListSerializer, CommentDetailSerializer

from note.models import Note


class CommentListView(generics.ListAPIView):
    def get_queryset(self):
        note_id = self.kwargs['notePk']
        note = get_object_or_404(Note, id=note_id, is_public=True)
        comments = Comment.objects.filter(note=note)
        return comments
    serializer_class = CommentListSerializer


class CommentCreateView(generics.ListCreateAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [permissions.PublicOrIsCommmentCreator]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            token = request.META["HTTP_AUTHORIZATION"].split()[1]
            user = Token.objects.get(key=token).user
            request.data["created_by"] = user.id
        except Token.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED,
                            data={"detail": "please login first"})
        response = super().post(request, *args, **kwargs)
        comment = get_object_or_404(Comment, id=response.data.get("id"))
        comment.note = get_object_or_404(Note, id=kwargs.get("notePk"))
        comment.save()
        response.data["note"] = comment.note.id
        return response


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        comment_id = self.kwargs['commentPk']
        comment = get_object_or_404(Comment, id=comment_id)
        if not self.request.method in rest_permissions.SAFE_METHODS:
            try:
                token = self.request.META["HTTP_AUTHORIZATION"].split()[1]
                current_user = Token.objects.get(key=token).user
                if current_user.id != comment.created_by.id:
                    return self.permission_denied(
                        self.request,
                        message="permission denied",
                        code=status.HTTP_403_FORBIDDEN
                    )
            except Token.DoesNotExist:
                return self.permission_denied(
                    self.request,
                    message="permission denied",
                    code=status.HTTP_403_FORBIDDEN
                )
        return comment

    serializer_class = CommentDetailSerializer
    permission_classes = [permissions.IsCommmentCreator]
    authentication_classes = [authentication.TokenAuthentication]

    def patch(self, request, *args, **kwargs):
        object = self.get_object()
        object.is_updated = True
        object.save()
        return super().patch(request, *args, **kwargs)
