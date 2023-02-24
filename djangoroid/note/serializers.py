from rest_framework import serializers

from note.models import Note, NoteToTag
from tag.models import Tag

def get_tag_note_objects(note):
    tags = NoteToTag.objects.filter(note=note)
    return tags



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
