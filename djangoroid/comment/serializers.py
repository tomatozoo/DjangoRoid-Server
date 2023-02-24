from rest_framework import serializers

from comment.models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'note', 'created_at', 'content',
                  'updated_at', 'is_updated', 'waffle_count']


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
