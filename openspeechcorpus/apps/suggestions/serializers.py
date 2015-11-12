from rest_framework import serializers

from . import models as suggestions_models
class SuggestionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = suggestions_models.Suggestion
        fields = (
            'suggestion',
            'user',
            'anonymous_user',
        )
