from rest_framework import permissions
from rest_framework import request as rest_request
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from note import models as note_models

def get_user(request):
    try:
        token = request.META["HTTP_AUTHORIZATION"].split()[1]
    except:
        return Response(f"invalid token", status=status.HTTP_401_UNAUTHORIZED)
    user = Token.objects.get(key=token).user
    return user

class PublicOrIsNoteCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: rest_request.Request, view, obj: note_models.Note):
        if request.method == "DELETE":
            return obj.created_by == request.user
        if obj.is_public:
            return True
        return obj.created_by == request.user


class IsNoteCreator(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request: rest_request.Request, view, obj: note_models.Note):
        print(obj.created_by, get_user(request))
        return obj.created_by == get_user(request)
    