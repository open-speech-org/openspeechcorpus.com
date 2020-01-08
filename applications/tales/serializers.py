from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError

from applications.core import serializers as core_serializers

from . import models as tales_models


class SimpleAuthorSerializer(ModelSerializer):
    class Meta:
        model = tales_models.Author
        fields = (
            'id',
            'name',
        )


class SimpleTaleSerializer(ModelSerializer):
    author = SimpleAuthorSerializer()

    class Meta:
        model = tales_models.Tale
        fields = (
            'title',
            'author',
        )


class TaleSerializer(ModelSerializer):
    author = SimpleAuthorSerializer()

    class Meta:
        model = tales_models.Tale
        fields = (
            'id',
            'title',
            'author',
            'description',
            'total_votes',
            'calification',
        )


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = tales_models.Author
        fields = (
            'id',
            'name',
            'biography',
            'birth',
            'death',
        )


class TaleSentenceSerializer(ModelSerializer):

    tale = SimpleTaleSerializer()

    class Meta:
        model = tales_models.TaleSentence
        fields = (
            'id',
            'tale',
            'text',
        )


class TaleVoteSerializer(ModelSerializer):
    class Meta:
        model = tales_models.TaleVote
        fields = (
            'calification',
            'opinion',
            'tale',
            'anonymous_user',
        )

    def validate_calification(self, value):
        if value < 0:
            raise ValidationError("Cannot take negative califications")
        if value > 5:
            raise ValidationError("Calification max value is 5.0")
        return value


class AnnotatedTaleSentenceSpeech(ModelSerializer):

    audio = core_serializers.AudioDataSerializer()
    tale_sentence = TaleSentenceSerializer()

    class Meta:
        model = tales_models.SentenceTaleSpeech
        fields = (
            'id',
            'audio',
            'tale_sentence',
        )
