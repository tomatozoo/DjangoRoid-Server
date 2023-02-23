from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from accounts.models import CustomUser as User
# from serializers import UserSerializer


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        username = request.data['username']
        # nickname = request.data['']
        password = request.data['password']
        try:
            user = User.objects.get(username=username)
            return Response(data={'detail' : f"{username} is already exist"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            user = User.objects.create(username=username, password=password)
            user.save()
            token = Token.objects.create(user=user)
            return Response(data={'detail' : f"id : {username} / pw : {password} user created"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        try:
            user = User.objects.get(username=username, password=password)
            token = Token.objects.get(user_id=user.id)
            content = {'token' : token.key,
                       'nickname' : user.nickname}
            return Response(data=content, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data={'detail' : f"No user matches. id : {username} pw : {password}"}, status=status.HTTP_200_OK)
        