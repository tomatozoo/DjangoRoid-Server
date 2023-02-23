from rest_framework import serializers

from tag import models as tag_models


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)

    class Meta:
        model = tag_models.Tag
        fields = "__all__"
