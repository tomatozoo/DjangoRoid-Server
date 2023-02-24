from rest_framework import serializers

from note.models import Note


class NoteListSerializer(serializers.ModelSerializer):
    # def to_representation(self, instance):
    #     rep_keys = ['title', 'desctiption']
    #     ret = {k:instance[k] for k in rep_keys}
    #     return super().to_representation(ret)
    class Meta:
        model = Note
        # field = '__all__'
        fields = ['id', 'title', 'description', 'waffle_count', 'fork_count',
                  'is_public', 'created_by', 'created_at', 'updated_at']


class NoteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        # field = ['title', 'description', 'waffle_count', 'fork_count', 'thumbnail', 'file', 'is_public', 'created_by', 'created_at', 'updated_at', 'history']
        # fields = ['title', 'description', 'waffle_count', 'fork_count', 'is_public', 'created_by', 'created_at', 'updated_at', 'history']
        fields = '__all__'
