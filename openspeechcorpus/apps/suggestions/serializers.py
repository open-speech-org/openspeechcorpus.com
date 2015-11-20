from rest_framework import serializers

from . import models as suggestions_models
from openspeechcorpus.apps.authentication import models as authentication_models

class SuggestionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = suggestions_models.Suggestion
        fields = (
            'suggestion',
            'user',
            'anonymous_user',
        )

    def create(self, validated_data):
        suggestion = suggestions_models.Suggestion(suggestion=validated_data['suggestion'])
        if validated_data.get('anonymous_user', None) is not None:
            suggestion.anonymous_user = validated_data['anonymous_user']

        suggestion.save()
        return suggestion