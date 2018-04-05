from rest_framework import serializers

from applications.core import serializers as core_serializer

from . import models


class Level(serializers.ModelSerializer):
    class Meta:
        model = models.Level
        fields = (
            'id',
            'title',
            'description'
        )


class LevelCategory(serializers.ModelSerializer):
    level = Level()

    class Meta:
        model = models.LevelCategory
        fields = (
            'id',
            'level',
            'title'
        )


class LevelSentence(serializers.ModelSerializer):
    level_category = LevelCategory()

    class Meta:
        model = models.LevelSentence
        fields = (
            'id',
            'level_category',
            'text'
        )


class LevelSentenceSpeech(serializers.ModelSerializer):
    level_sentence = LevelSentence()
    audio = core_serializer.AudioDataSerializer

    class Meta:
        model = models.LevelSentenceSpeech
        fields = (
            'id',
            'level_sentence',
            'audio'
        )
