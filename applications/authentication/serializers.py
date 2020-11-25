from rest_framework import serializers

from .models import AnonymousUserProfile


class AnonymousUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousUserProfile
        fields = (
            'anonymous_name',
            'gender',
            'age',
            'accent',
            'pitch',
            'height',
            'weight',
        )
