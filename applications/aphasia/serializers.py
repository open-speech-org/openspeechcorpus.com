from rest_framework import serializers

from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from applications.core import serializers as core_serializer

from . import models

from applications.authentication import (
    models as authentication_models
)

from applications.core import (
    models as core_models,
    serializers as core_serializers
)



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


class LevelSentenceSpeech(serializers.Serializer):
    anonymous_user = serializers.IntegerField(required=False)
    level_sentence_id = serializers.IntegerField()
    text = serializers.CharField(max_length=10000, required=False)
    audio = serializers.FileField()

    def create(self, validated_data):
        level_sentence_id = validated_data.get('level_sentence_id', 0)
        audio_file = validated_data.get('audio', None)
        if audio_file is None:
            raise serializers.ValidationError(_('Audio data is not defined'))
        try:
            print("Level Sentence ID", level_sentence_id)
            level_sentence = models.LevelSentence.objects.get(pk=level_sentence_id)
            name = level_sentence.text
            element_count = core_models.AudioData.objects.filter(name__icontains=name).count()
            slug = slugify("{} {}".format(name[:40], str(element_count)))
            print(slug)
            print(len(slug))
            audio_data = core_models.AudioData(
                name=name,
                slug=slug,
                text=level_sentence.text,
                audiofile=audio_file
            )
            audio_data.save()
            tale_sentence_speech = models.LevelSentenceSpeech(
                level_sentence=level_sentence,
                audio=audio_data

            )
            tale_sentence_speech.save()
            anonymous_id = validated_data.get('anonymous_user', False)
            if anonymous_id:
                print(anonymous_id)
                print("Exists")
                try:
                    anonymous_profile = authentication_models.AnonymousUserProfile.objects.get(pk=anonymous_id)
                    anonymous_audio_data = core_models.AnonymousAudioData(
                        audio=audio_data,
                        user=anonymous_profile
                    )
                    anonymous_audio_data.save()
                    print(anonymous_audio_data)
                except authentication_models.AnonymousUserProfile.DoesNotExist:
                    print("Anonymous does not exists")

            else:
                print("NO ANONIMOUS ID")

            return audio_data

        except models.LevelSentence.DoesNotExist:
            raise serializers.ValidationError(_('Tale sentence Does not exists'))


class LevelSentenceText(serializers.ModelSerializer):
    class Meta:
        model = models.LevelSentence
        fields = (
            'text',
        )


class AnnotatedLevelSentenceSpeech(serializers.ModelSerializer):

    audio = core_serializer.AudioDataSerializer()
    level_sentence = LevelSentenceText()

    class Meta:
        model = models.LevelSentenceSpeech
        fields = (
            'id',
            'audio',
            'level_sentence',
        )
