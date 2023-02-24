from rest_framework import serializers

from note.models import Note, NoteToTag, Canvas, Page
from tag.models import Tag


def get_tag_note_objects(note):
    tags = NoteToTag.objects.filter(note=note)
    return tags


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class CanvasSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Canvas
        fields = ("id", "created_at", "updated_at", "pages")


class NoteListSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        tags = get_tag_note_objects(instance)
        ret['tags'] = [tag.tag.name for tag in tags]
        return ret

    class Meta:
        model = Note
        fields = ['id', 'title', 'description', 'waffle_count', 'fork_count',
                  'is_public', 'created_by', 'created_at', 'updated_at']


class NoteDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        tags = get_tag_note_objects(instance)
        ret['tags'] = [tag.tag.name for tag in tags]
        return ret

    class Meta:
        model = Note
        fields = '__all__'
