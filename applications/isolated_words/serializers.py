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


class Category(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = (
            'id',
            'title',
            'description'
        )


class IsolatedWord(serializers.ModelSerializer):
    category = Category()

    class Meta:
        model = models.IsolatedWord
        fields = (
            'id',
            'category',
            'text'
        )


class IsolatedWordSpeech(serializers.Serializer):
    anonymous_user = serializers.IntegerField(required=False)
    isolated_word_id = serializers.IntegerField()
    text = serializers.CharField(max_length=10000, required=False)
    audio = serializers.FileField()

    def create(self, validated_data):
        isolated_word_id = validated_data.get('isolated_word_id', 0)
        audio_file = validated_data.get('audio', None)
        if audio_file is None:
            raise serializers.ValidationError(_('Audio data is not defined'))
        try:
            print("Isolated Word ID", isolated_word_id)
            isolated_word = models.IsolatedWord.objects.get(pk=isolated_word_id)
            name = isolated_word.text
            element_count = core_models.AudioData.objects.filter(name__icontains=name).count()
            slug = slugify("{} {}".format(name[:40], str(element_count)))
            print(slug)
            print(len(slug))
            audio_data = core_models.AudioData(
                name=name,
                slug=slug,
                text=isolated_word.text,
                audiofile=audio_file
            )
            audio_data.save()
            isolated_word_speech = models.IsolatedWordSpeech(
                isolated_word=isolated_word,
                audio=audio_data

            )
            isolated_word_speech.save()
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

        except models.IsolatedWord.DoesNotExist:
            raise serializers.ValidationError(_('Isolated word Does not exists'))


class IsolatedWordText(serializers.ModelSerializer):
    class Meta:
        model = models.IsolatedWord
        fields = (
            'text',
        )


class AnnotatedIsolatedWordSpeech(serializers.ModelSerializer):

    audio = core_serializer.AudioDataSerializer()
    isolated_word = IsolatedWordText()

    class Meta:
        model = models.IsolatedWordSpeech
        fields = (
            'id',
            'audio',
            'isolated_word',
        )
