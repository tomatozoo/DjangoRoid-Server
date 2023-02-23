from rest_framework import permissions
from rest_framework import request as rest_request

from note import models as note_models


class PublicOrIsNoteCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: rest_request.Request, view, obj: note_models.Note):
        if request.method == "DELETE":
            return obj.created_by == request.user
        if obj.is_public:
            return True
        return obj.created_by == request.user


class IsNoteCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: rest_request.Request, view, obj: note_models.Note):
        return obj.created_by == request.user


class IsNotePublicAndCommentCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: rest_request.Request, view, obj: note_models.Comment):
        if obj.note.is_public:
            return True
        return obj.note.created_by == request.user


class IsCommentCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: rest_request.Request, view, obj: note_models.Note):
        return obj.created_by == request.user
