from rest_framework import generics
from rest_framework.filters import SearchFilter

from note import models
from note import serializers


class SearchView(generics.ListAPIView):
    queryset = models.Note.objects.all()
    serializer_class = serializers.NoteListSerializer

    filter_backends = [SearchFilter]
    search_fields = ["title", "description"]
