from rest_framework import serializers

from comment import models as comment_models


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comment_models.Comment
        fields = "__all__"
        extra_kwargs = {
            "created_by": {
                "default": serializers.CurrentUserDefault(),
            },
        }
