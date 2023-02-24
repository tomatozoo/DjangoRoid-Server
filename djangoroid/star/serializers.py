from rest_framework import serializers

from star.models import Waffle

class WaffleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waffle
        fields = "__all__"
