from typing import Dict

from django import shortcuts
from rest_framework import serializers

from note import models as note_models
from tag import serializers as tag_serializers


class NoteSerializer(serializers.ModelSerializer):
    tags = tag_serializers.TagSerializer(many=True, required=False)

    class Meta:
        model = note_models.Note
        fields = "__all__"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
            },
        }

    def create(self, validated_data: Dict):
        tag_data_list = validated_data.pop("tags", [])
        note = super().create(validated_data)

        for tag_data in tag_data_list:
            tag, _ = shortcuts.get_object_or_404(note_models.Tag, **tag_data)
            note_models.TagToNote.objects.create(note=note, tag=tag)
        return note
