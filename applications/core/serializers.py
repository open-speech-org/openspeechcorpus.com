# -*- coding: UTF-8 -*-
import random
import string

from rest_framework import serializers
from django.utils.text import slugify

from . import models as core_models
from applications.authentication.serializers import AnonymousUserProfileSerializer


class AudioDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = core_models.AudioData
        fields = (
            'id',
            'text',
            'audiofile',
        )

    def create(self, validated_data):
        text = validated_data.get('text', "")
        audiofile = validated_data.get('audiofile', None)
        if audiofile is not None:
            name = ' '.join(text.split()[:5])
            slug = slugify(text+" "+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)))
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


class AnonymousAudioDataSerializer(serializers.ModelSerializer):
    user = AnonymousUserProfileSerializer()

    class Meta:
        model = core_models.AnonymousAudioData
        fields = (
            'user',
        )


class FullDetailAudioData(serializers.ModelSerializer):
    anonymous_profile = AnonymousAudioDataSerializer(source='anonymousaudiodata_set', many=True)

    class Meta:
        model = core_models.AudioData
        fields = (
            'id',
            'text',
            'audiofile',
            'anonymous_profile'
        )
