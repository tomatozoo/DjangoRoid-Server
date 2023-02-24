from django.shortcuts import render, resolve_url, redirect, get_object_or_404
from django.contrib import auth

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.parsers import JSONParser

from accounts.models import CustomUser as User
from accounts.models import UserToTag
from tag.models import Tag

BASE_URL = "http://127.0.0.1/"


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']

        try:
            user = User.objects.get(username=username)
            return Response(data={'detail': f"{username} is already exist"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            nickname = request.data['nickname'] if 'nickname' in request.data else "Anonymous"
            user = User.objects.create(
                username=username, password=password, nickname=nickname)
            user.save()
            for tag in request.data['tags']:
                UserToTag.objects.create(
                    tag=Tag.objects.get(name=tag), user=user)
            return Response(data={'detail': f"id : {username} / pw : {password} user created"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=username, password=password)
            token = Token.objects.create(user=user)
            token.save()
            token = Token.objects.get_or_create(user_id=user.id)
            user_to_tag = UserToTag.objects.filter(user=user)
            tags = [str(utt.tag) for utt in user_to_tag]
            content = {'token': token.key,
                       'user': {'id': user.id,
                                'username': user.username,
                                'nickname': user.nickname,
                                'tags': tags}}
            return Response(data=content, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data={'detail': f"User not found. id : {username} pw : {password}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    auth.logout(request)
    key = request.data['key']
    token = Token.objects.get(key=key)
    token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        token = request.META["HTTP_AUTHORIZATION"].split()[1]
        user = Token.objects.get(key=token).user

        user_to_tag = UserToTag.objects.filter(user=user)
        tags = [str(utt.tag) for utt in user_to_tag]
        content = {'token': token.key,
                   'user': {'id': user.id,
                            'username': user.username,
                            'nickname': user.nickname,
                            'tags': tags}}
        return Response(data=content, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            token = request.META["HTTP_AUTHORIZATION"].split()[1]
            user = Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED,
                            data={"detail": "pleas log in first"})

        username = request.data.get("username")
        tags = request.data.get("tags")
        nickname = request.data.get("nickname")

        if (tags is not None):
            UserToTag.objects.filter(user=user).delete()
            for tag in tags:
                tag_object = get_object_or_404(Tag, name=tag)
                UserToTag.objects.create(user=user, tag=tag_object)

        if (nickname is not None):
            user.nickname = nickname
            user.save()

        if (username is not None) and User.objects.filter(username=username).count() != 0:
            users = User.objects.filter(username=username)
            print(users)
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"detail": "username already exists"})

        user_to_tag = UserToTag.objects.filter(user=user)
        tags = [str(utt.tag) for utt in user_to_tag]
        content = {'id': user.id,
                   'username': user.username,
                   'nickname': user.nickname,
                   'tags': tags}
        return Response(data=content, status=status.HTTP_200_OK)
