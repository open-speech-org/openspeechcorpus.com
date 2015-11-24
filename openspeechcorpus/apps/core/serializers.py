# -*- coding: UTF-8 -*-
from rest_framework import serializers
from django.utils.text import slugify

from . import models as core_models

class AudioDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.AudioData
        fields = (
            'text',
            'audiofile',
        )

    def create(self, validated_data):
        text = validated_data.get('text', "")
        audiofile = validated_data.get('audiofile', None)
        if audiofile is not None:
            name = ' '.join(text.split()[:5])
            slug = slugify(text)
            audio_data = core_models.AudioData(
                name=name,
                slug=slug,
                text=text,
                audiofile=audiofile
            )
            audio_data.save()
            return audio_data
        else:
            return None
