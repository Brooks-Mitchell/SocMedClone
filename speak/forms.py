import re
from unittest.util import _MAX_LENGTH
from django import forms
from .models import Speak

MAX_SPEAK_LENGTH = 360

class SpeakForm(forms.ModelForm):
    class Meta:
        model = Speak
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_SPEAK_LENGTH:
            raise forms.ValidationError("This is too long")
        return content