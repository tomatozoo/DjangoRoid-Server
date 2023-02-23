from rest_framework import permissions
from rest_framework import request as rest_request

from comment import models as comment_models


class IsCommentCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: rest_request.Request, view, obj: comment_models.Comment):
        return obj.created_by == request.user


class IsNotePublicAndCommentCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: rest_request.Request, view, obj: comment_models.Comment):
        if obj.note.is_public:
            return True
        return obj.note.created_by == request.user
