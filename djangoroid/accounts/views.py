from django.shortcuts import render, resolve_url, redirect
from django.contrib import auth

from rest_framework.decorators import api_view
from rest_framework.response import Response
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
            return Response(data={'detail' : f"{username} is already exist"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            nickname = request.data['nickname'] if 'nickname' in request.data else "Anonymous"
            user = User.objects.create(username=username, password=password, nickname=nickname)
            user.save()
            for tag in request.data['tags']:
                UserToTag.objects.create(tag=Tag.objects.get(name=tag), user=user)
            return Response(data={'detail' : f"id : {username} / pw : {password} user created"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=username, password=password)
            token = Token.objects.create(user=user)
            token.save()
            token = Token.objects.get(user_id=user.id)
            user_to_tag = UserToTag.objects.filter(user=user)
            tags = [str(utt.tag) for utt in user_to_tag]
            content = {'token' : token.key,
                       'user' : {'id' : user.id,
                        'username' : user.username,
                        'nickname' : user.nickname,
                        'tags' : tags}}
            return Response(data=content, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data={'detail' : f"User not found. id : {username} pw : {password}"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    auth.logout(request)
    key = request.data['key']
    token = Token.objects.get(key=key)
    token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
