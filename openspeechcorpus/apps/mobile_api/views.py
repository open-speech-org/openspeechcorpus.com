from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers as mobile_api_serializer

from openspeechcorpus.apps.tales import serializers as tales_serializers
from openspeechcorpus.apps.tales import models as tales_models
from openspeechcorpus.apps.authentication import models as authentication_models
from openspeechcorpus.apps.suggestions import serializers as suggestions_serializers
from openspeechcorpus.apps.core import serializers as core_serializers
from openspeechcorpus.apps.core import models as core_models


# Create your views here.
class TalesSentencesView(APIView):

    def get(self, request, format=None):

        offset = int(request.query_params.get('offset', 0))
        sentences = tales_models.TaleSentence.objects.all()[offset:offset+10]
        sentences_serialized = tales_serializers.TaleSentenceSerializer(data=sentences, many=True)
        sentences_serialized.is_valid()
        print sentences_serialized.data

        if request.query_params.get('new_user', False):
            print "New user requested"
            anonymous_user = authentication_models.AnonymousUserProfile(
                anonymous_name='anonymous_'+unicode(authentication_models.AnonymousUserProfile.objects.all().count())
            )
            anonymous_user.save()
            print anonymous_user
            anonymous_user_sentence_serialized = mobile_api_serializer.AnonymousUserSentenceSerializer(
                data={
                    'anonymous_user': anonymous_user.id,
                    'sentences': sentences_serialized.data
                }
            )
            print anonymous_user_sentence_serialized.is_valid()
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
            return Response(
                {
                    'state': 'Success',
                    'error': 0
                }
                )
        else:
            print("False")
            return Response(
                {
                    'state': 'Failure',
                    'error': 1
                }
            )

class RegisterSuggestion(APIView):

    def post(self, request, format=None):
        suggestion_serializer = suggestions_serializers.SuggestionModelSerializer(data=request.data)

        if suggestion_serializer.is_valid(True):
            suggestion_serializer.save()
            print("True")
            return Response(suggestion_serializer.data)
        else:
            return Response(
                {
                    'state': 'Failure',
                    'error': 1
                }
            )

class UpdateAnonymousUserProfile(APIView):

    def post(self, request, format=None):
        anonymous_id = request.data.get('anonymous_user', None)

        if anonymous_id is not None:
            anonymous_new_name = request.data.get('anonymous_user_name', None)
            anonymous_new_picture = request.data.get('anonymous_user_picture', None)
            try:
                anonymous_user_profile = authentication_models.AnonymousUserProfile.objects.get(pk=anonymous_id)
                print(anonymous_user_profile)
                if anonymous_new_name is not None:
                    anonymous_user_profile.anonymous_name = anonymous_new_name
                if anonymous_new_picture is not None:
                    anonymous_user_profile.anonymous_picture = anonymous_new_picture
                anonymous_user_profile.save()
                anonymous_user_profile_history = authentication_models.AnonymousUserProfileHistory(
                    anonymous_user_profile=anonymous_user_profile,
                    anonymous_name=anonymous_new_name,
                    anonymous_picture=anonymous_new_picture
                )
                anonymous_user_profile_history.save()
                return Response(
                    {
                        'state': 'Anonymous User Profile updated',
                        'error': 0
                    }
                )

            except authentication_models.AnonymousUserProfile.DoesNotExist:
                return Response(
                    {
                        'state': 'Anonymous User Profile not found',
                        'error': 404
                    }
                )
        else:
            return Response(
                {
                    'state': 'anonymous_user must be defined',
                    'error': 1
                }
            )



class UploadCustomAudio(APIView):

    def post(self,request, format=None):
        print request.data
        audio_serializer = core_serializers.AudioDataSerializer(data=request.data)
        if audio_serializer.is_valid(True):
            audio_data = audio_serializer.save()
            print(audio_data)
            anonymous_user_id = request.data.get('anonymous_user', None)
            if anonymous_user_id is not None:
                try:
                    anonymous_user = authentication_models.AnonymousUserProfile.objects.get(pk=anonymous_user_id)
                    anonymous_audio_data = core_models.AnonymousAudioData(
                        audio=audio_data,
                        user=anonymous_user
                    )
                    anonymous_audio_data.save()
                except authentication_models.AnonymousUserProfile.DoesNotExist:
                    return Response(
                        {
                            'state': 'Anonimous User not defined',
                            'error': 0
                        }
                    )
            return Response(
                {
                    'state': 'Success',
                    'error': 0
                }
            )
        else:
            return Response(
                {
                    'state': 'Incomplete',
                    'error': 1
                }
            )