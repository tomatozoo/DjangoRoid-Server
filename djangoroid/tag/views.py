from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from tag.models import Tag
from tag.serializers import TagSerializer
# Create your views here.

class TagListCreateView(ListCreateAPIView):
    def get_queryset(self):
        queryset = Tag.objects.all()
        return queryset

    def perform_create(self, serializer):
        tag_name = self.request.data['name']
        serializer.save(name=tag_name)
    
    serializer_class = TagSerializer


class TagDestoryView(DestroyAPIView):
    def get_object(self):
        tid = self.kwargs['tid']
        try:
            tag = Tag.objects.get(id=tid)
        except Tag.DoesNotExist:
            return Response({'detail' : f'No tag matches. {tid}'}, status=status.HTTP_200_OK)
        return tag

    serializer_class = TagSerializer