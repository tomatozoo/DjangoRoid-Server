from django.shortcuts import render, get_object_or_404

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from star.models import Waffle, CommentWaffle, NoteWaffle
from star.serializers import WaffleListSerializer

from note.models import Note
from comment.models import Comment

from django.contrib.auth import get_user_model  
User = get_user_model()

def get_user(request):
    try:
        token = request.META["HTTP_AUTHORIZATION"].split()[1]
    except:
        return Response(f"invalid token", status=status.HTTP_401_UNAUTHORIZED)
    user = Token.objects.get(key=token).user
    return user


def ViewFunctionFactory(model_class, waffle_class, pk):
    @api_view(["GET", "POST", "DELETE"])
    def view(request, *args, **kwargs):
        if request.method == "GET":
            id = kwargs[pk]
            obj = get_object_or_404(model_class, id=id)
            waffles = waffle_class.objects.filter(obj=obj)
            serializer = WaffleListSerializer(waffles, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == "POST":
            user = get_user(request)
            if not isinstance(user, User):
                return user

            id = kwargs[pk]
            obj = get_object_or_404(model_class, id=id)

            try:
                waffle_class.objects.get(obj=obj, created_by=user)
                return Response(data={'detail': f'user {user.id} already waffled this object.'},
                                status=status.HTTP_400_BAD_REQUEST)
            except waffle_class.DoesNotExist:
                waffle = waffle_class.objects.create(obj=obj, created_by=user)
                waffle.save()
                obj.waffle_count += 1
                obj.save()
                return Response(data={'detail': f'user {user.id} waffled this object.'},
                                status=status.HTTP_201_CREATED)
            
        elif request.method == "DELETE":
            user = get_user(request)
            if not isinstance(user, User):
                return user
            
            id = kwargs[pk]
            obj = get_object_or_404(model_class, id=id)
            obj.waffle_count -= 1
            obj.save()
            
            waffle = get_object_or_404(waffle_class, obj=obj, created_by=user)
            waffle.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    return view

note_waffle_view = ViewFunctionFactory(Note, NoteWaffle, "notePk")
comment_waffle_view = ViewFunctionFactory(Comment, CommentWaffle, "commentPK")
