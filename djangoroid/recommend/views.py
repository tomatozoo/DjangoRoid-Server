from django.shortcuts import render

from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from note import models as note_models
from accounts import models as account_models
from note import serializers
from recommend import paginations


class RecommendView(ListAPIView):
    queryset = note_models.Note.objects.all()
    serializer_class = serializers.NoteListSerializer
    pagination_class = paginations.NoteListPagination
