from rest_framework import serializers
from django.conf import settings
from .models import Speak

MAX_SPEAK_LENGTH = settings.MAX_SPEAK_LENGTH

class SpeakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speak
        fields = ['content']

    def validate_content(self, value):
        if len(value) > MAX_SPEAK_LENGTH:
            raise serializers.ValidationError("This is too long")
        return value