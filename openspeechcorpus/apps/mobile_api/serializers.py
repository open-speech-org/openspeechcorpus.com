# -*- coding: UTF-8 -*-

from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from openspeechcorpus.apps.tales import serializers as tales_serializers
from openspeechcorpus.apps.tales import models as tales_models
from openspeechcorpus.apps.core import models as core_models
from openspeechcorpus.apps.core import serializers as core_serializer
from openspeechcorpus.apps.authentication import models as authentication_models



class AnonymousUserSentenceSerializer(serializers.Serializer):
    anonymous_user = serializers.IntegerField()
    sentences = tales_serializers.TaleSentenceSerializer()

class AnonymousUserCustomAudioSerializer(serializers.Serializer):
    anonymous_user = serializers.IntegerField()
    audio = core_serializer.AudioDataSerializer()


class AudioTaleSentenceUploadSerializer(serializers.Serializer):
    anonymous_user = serializers.IntegerField(required=False)
    tale_sentence_id = serializers.IntegerField()
    text = serializers.CharField(max_length=10000, required=False)
    audio = serializers.FileField()

    def create(self, validated_data):
        tale_sentence_id = validated_data.get('tale_sentence_id', 0)
        audio_file = validated_data.get('audio', None)
        if audio_file is None:
            raise serializers.ValidationError(_('Audio data is not defined'))
        try:
            tale_sentence = tales_models.TaleSentence.objects.get(pk=tale_sentence_id)
            name = tale_sentence.tale.title + " " + unicode(tale_sentence.place)
            element_count = core_models.AudioData.objects.filter(name__icontains=name).count()
            audio_data = core_models.AudioData(
                name=name,
                slug=slugify(name+" "+unicode(element_count)),
                text=tale_sentence.text,
                audiofile=audio_file
            )
            audio_data.save()
            tale_sentence_speech = tales_models.SentenceTaleSpeech(
                tale_sentence=tale_sentence,
                audio=audio_data

            )
            tale_sentence_speech.save()
            anonymous_id = validated_data.get('anonymous_user', False)
            if anonymous_id:
                print anonymous_id
                print "Exists"
                try:
                    anonymous_profile = authentication_models.AnonymousUserProfile.objects.get(pk=anonymous_id)
                    anonymous_audio_data = core_models.AnonymousAudioData(
                        audio=audio_data,
                        user=anonymous_profile
                    )
                    anonymous_audio_data.save()
                    print anonymous_audio_data
                except authentication_models.AnonymousUserProfile.DoesNotExist:
                    print("Anonymous does not exists")

            else:
                print("NO ANONIMOUS ID")

            return audio_data

        except tales_models.TaleSentence.DoesNotExist:
            raise serializers.ValidationError(_('Tale sentence Does not exists'))
