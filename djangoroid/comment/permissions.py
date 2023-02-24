from rest_framework import permissions
from rest_framework import request as rest_request

from comment import models as comment_models


class PublicOrIsCommmentCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: rest_request.Request, view, obj: comment_models.Comment):
        if request.method in permissions.SAFE_METHODS:
            # 읽는 것은 누구나 할 수 있음
            return True
        # 생성/수정을 하고자 하는 경우 생성한 사람이어야 함
        return obj.created_by == request.user


class IsCommmentCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: rest_request.Request, view, obj: comment_models.Comment):
        return obj.created_by == request.user
