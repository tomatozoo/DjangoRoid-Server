from typing import Dict

from django import shortcuts
from rest_framework import serializers

from waffle import models as waffle_models


class WaffleSerializer(serializers.ModelSerializer):
    class Meta:
        model = waffle_models.Waffle
        fields = "__all__"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
            },
        }

    def create(self, validated_data: Dict):
        waffle = super().create(validated_data)
        note = shortcuts.get_object_or_404(waffle_models.Note, pk=waffle.note.pk)
        note.waffle_count += 1
        note.save()
