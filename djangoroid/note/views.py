from django.shortcuts import render
from rest_framework import authentication
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import request as req
from rest_framework import response
from rest_framework import status
from rest_framework import views

from note import models as note_models
from note import paginations as note_paginations
from note import permissions as note_permissions
from note import serializers as note_serializers


class NoteListCreateView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = note_paginations.NoteListPagination
    permission_classes = [note_permissions.PublicOrIsNoteCreator]
    queryset = note_models.Note.objects.all()
    serializer_class = note_serializers.NoteSerializer


class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [note_permissions.PublicOrIsNoteCreator]
    queryset = note_models.Note.objects.all()
    serializer_class = note_serializers.NoteSerializer
    lookup_field = "nid"


class CommentListCreateView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = note_paginations.CommentListPagination
    permission_classes = [note_permissions.PublicOrIsNoteCreator]
    queryset = note_models.Comment.objects.all()
    serializer_class = note_serializers.CommentSerializer

    def post(self, request: req.Request, *args, **kwargs):
        request.data["note"] = kwargs.get("nid")
        return super().post(request, *args, **kwargs)

    def get(self, request: req.Request, *args, **kwargs):
        request.data["note"] = kwargs.get("nid")
        return super().get(request, *args, **kwargs)


class CommentUpdateDestroyView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [note_permissions.IsCommentCreator]
    queryset = note_models.Comment.objects.all()
    serializer_class = note_serializers.CommentSerializer
    lookup_field = "cid"

    def put(self, request: req.Request, *args, **kwargs):
        request.data["post"] = kwargs.get("pid")
        return self.update(request, *args, **kwargs)

    def patch(self, request: req.Request, *args, **kwargs):
        request.data["post"] = kwargs.get("pid")
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: req.Request, *args, **kwargs):
        request.data["post"] = kwargs.get("pid")
        return self.destroy(request, *args, **kwargs)


class NoteForkCreateView:
    pass


class WaffleListCreateView:
    pass
