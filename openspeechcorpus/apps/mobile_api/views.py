from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers as mobile_api_serializer

from openspeechcorpus.apps.tales import serializers as tales_serializers
from openspeechcorpus.apps.tales import models as tales_models
from openspeechcorpus.apps.authentication import models as authentication_models


# Create your views here.
class TalesSentencesView(APIView):

    def get(self, request, format=None):

        offset = int(request.query_params.get('offset', 0))
        sentences = tales_models.TaleSentence.objects.all()[offset:offset+10]
        sentences_serialized = tales_serializers.TaleSentenceSerializer(data=sentences, many=True)
        sentences_serialized.is_valid()
        print sentences_serialized.data

        if request.query_params.get('new_user', False):
            anonymous_user = authentication_models.AnonymousUserProfile(
                anonymous_name='anonymous_'+unicode(authentication_models.AnonymousUserProfile.objects.all().count())
            )
            anonymous_user.save()
            anonymous_user_sentence_serialized = mobile_api_serializer.AnonymousUserSentenceSerializer(
                data={
                    'anonymous_id': anonymous_user.id,
                    'sentences': sentences_serialized.data
                }
            )
            anonymous_user_sentence_serialized.is_valid()
            print anonymous_user_sentence_serialized.data
            return Response(anonymous_user_sentence_serialized.data)
        else:

            return Response(sentences_serialized.data)


class UploadTaleSetenceView(APIView):
    def post(self, request, format=None):
        print request.data
        audio_upload_tale_data = mobile_api_serializer.AudioTaleSentenceUploadSerializer(data=request.data)

        if audio_upload_tale_data.is_valid(True):
            print("True")
            audio_upload_tale_data.save()
            return Response({
                'state': 'Success',
                'error': 0
            })
        else:
            print("False")
            return Response({
                'state': 'Failure',
                'error': 1
            })
