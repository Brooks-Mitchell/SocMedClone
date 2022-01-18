import re
from unittest.util import _MAX_LENGTH
from django import forms
from .models import Speak
from django.conf import settings

MAX_SPEAK_LENGTH = settings.MAX_SPEAK_LENGTH

class SpeakForm(forms.ModelForm):
    class Meta:
        model = Speak
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_SPEAK_LENGTH:
            raise forms.ValidationError("This is too long")
        return content