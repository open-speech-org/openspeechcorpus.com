from rest_framework import serializers

from . import models as news_models

class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = news_models.New
        fields = (
            'id',
            'title',
            'body'
        )
