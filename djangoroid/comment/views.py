from django.shortcuts import render
from rest_framework import authentication
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import request as req
from rest_framework import response
from rest_framework import status
from rest_framework import views

from comment import models as comment_models
from comment import paginations as comment_paginations
from comment import permissions as comment_permissions
from comment import serializers as comment_serializers


class CommentListCreateView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = comment_paginations.CommentListPagination
    permission_classes = [comment_permissions.PublicOrIsNoteCreator]
    queryset = comment_models.Comment.objects.all()
    serializer_class = comment_serializers.CommentSerializer

    def post(self, request: req.Request, *args, **kwargs):
        request.data["note"] = kwargs.get("nid")
        return super().post(request, *args, **kwargs)

    def get(self, request: req.Request, *args, **kwargs):
        request.data["note"] = kwargs.get("nid")
        return super().get(request, *args, **kwargs)


class CommentUpdateDestroyView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [comment_permissions.IsCommentCreator]
    queryset = comment_models.Comment.objects.all()
    serializer_class = comment_serializers.CommentSerializer
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
