from django import forms
from applications.authentication.models import AnonymousUserProfile


class SpeakerCharacterization(forms.ModelForm):
    class Meta:
        model = AnonymousUserProfile
        widgets = {
            'gender': forms.Select(attrs={"class": "browser-default"})
        }
        fields = (
            'gender',
            'age',
            'accent',
            'pitch',
            'height',
            'weight'
        )
