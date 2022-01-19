from rest_framework import serializers
from django.conf import settings
from .models import Speak

MAX_SPEAK_LENGTH = settings.MAX_SPEAK_LENGTH
SPEAK_ACTION_OPTIONS = settings.SPEAK_ACTION_OPTIONS

class speakActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in SPEAK_ACTION_OPTIONS:
            raise serializers.ValidationError("Not a valid action")
        return value

class SpeakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speak
        fields = ['content']

    def validate_content(self, value):
        if len(value) > MAX_SPEAK_LENGTH:
            raise serializers.ValidationError("This is too long")
        return value