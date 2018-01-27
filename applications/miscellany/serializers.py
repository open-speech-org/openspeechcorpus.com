from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from . import models as miscellany_models
from applications.core import models as core_models
from applications.authentication import models as authentication_models



class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = miscellany_models.Command
        fields = (
            'id',
            'text',
        )

class AnonymousCommandSerializer(serializers.Serializer):
    anonymous_user = serializers.IntegerField()
    commands = CommandSerializer()

class CommandUploadSerializer(serializers.Serializer):
    anonymous_user = serializers.IntegerField(required=False)
    command_id = serializers.IntegerField()
    text = serializers.CharField(max_length=10000, required=False)
    audio = serializers.FileField()

    def create(self, validated_data):
        command_id = validated_data.get('command_id', 0)
        audio_file = validated_data.get('audio', None)
        if audio_file is None:
            raise serializers.ValidationError(_('Audio data is not defined'))
        try:
            command = miscellany_models.Command.objects.get(pk=command_id)
            name = command.text
            element_count = core_models.AudioData.objects.filter(name__icontains=name).count()
            audio_data = core_models.AudioData(
                name=name,
                slug=slugify(name+" "+unicode(element_count)),
                text=command.text,
                audiofile=audio_file
            )
            audio_data.save()
            command_speech = miscellany_models.CommandSpeech(
                command=command,
                audio=audio_data

            )
            command_speech.save()
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

        except miscellany_models.Command.DoesNotExist:
            raise serializers.ValidationError(_('Command Does not exists'))
