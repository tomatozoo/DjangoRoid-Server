from django.shortcuts import render, resolve_url, redirect
from django.contrib import auth

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from accounts.models import CustomUser as User

BASE_URL = "http://127.0.0.1/"

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']

        try:
            user = User.objects.get(username=username)
            # return Response(data={'detail' : f"{username} is already exist"}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create(**request.data)
            user.save()
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
            content = {'token' : token.key,
                       'nickname' : user.nickname}
            return Response(data=content, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # return Response(data={'detail' : f"No user matches. id : {username} pw : {password}"}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    auth.logout(request)
    key = request.data['key']
    token = Token.objects.get(key=key)
    token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
