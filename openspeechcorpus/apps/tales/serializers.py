from rest_framework.serializers import ModelSerializer

from . import models as tales_models

class SimpleAuthorSerializer(ModelSerializer):
    class Meta:
        model = tales_models.Author
        fields = (
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


class TaleSentenceSerializer(ModelSerializer):

    tale = SimpleTaleSerializer()

    class Meta:
        model = tales_models.TaleSentence
        fields = (
            'id',
            'tale',
            'text',
        )
