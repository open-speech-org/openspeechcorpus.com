import random
from itertools import chain

from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView



from . import serializers as mobile_api_serializer
from applications.tales import serializers as tales_serializers
from applications.tales import models as tales_models
from applications.authentication import models as authentication_models
from applications.suggestions import serializers as suggestions_serializers
from applications.core import serializers as core_serializers
from applications.core import models as core_models


# Create your views here.
class TalesSentencesView(APIView):

    def get(self, request, format=None):

        offset = int(request.query_params.get('offset', 0))
        if offset == 0:
            random_tale = random.random()*tales_models.Tale.objects.count()
            tale_sentences = tales_models.TaleSentence.objects.filter(tale__id=random_tale)
            offset = tale_sentences[0].id - 1
        sentences = tales_models.TaleSentence.objects.all()[offset:offset+10]
        sentences_serialized = tales_serializers.TaleSentenceSerializer(data=sentences, many=True)
        sentences_serialized.is_valid()
        print(sentences_serialized.data)

        if request.query_params.get('new_user', False):
            print("New user requested")
            anonymous_user = authentication_models.AnonymousUserProfile(
                anonymous_name='anonymous_{}'.format(
                    str(authentication_models.AnonymousUserProfile.objects.all().count()
                        )
                )
            )
            anonymous_user.save()
            print(anonymous_user)
            anonymous_user_sentence_serialized = mobile_api_serializer.AnonymousUserSentenceSerializer(
                data={
                    'anonymous_user': anonymous_user.id,
                    'sentences': sentences_serialized.data
                }
            )
            print(anonymous_user_sentence_serialized.is_valid())

            print(anonymous_user_sentence_serialized.data)
            return Response(anonymous_user_sentence_serialized.data)
        else:

            return Response(sentences_serialized.data)


class UploadTaleSetenceView(APIView):
    def post(self, request, format=None):
        print(request.data)
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
        print(request.data)
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

class GetTales(APIView):

    def get(self, request, format=None):
        offset = request.query_params.get('offset', 0)
        all_tales = tales_models.Tale.objects.filter(pk__gt=offset)
        serializer = tales_serializers.TaleSerializer(all_tales, many=True)

        return Response(
            {
                'state': 'Success',
                'error': 0,
                'tales': serializer.data
            }
        )
        # else:
        #     return Response(
        #         {
        #             'state': 'Failure',
        #             'error': 1
        #         }
        #     )



class GetAuthors(APIView):

    def get(self, request, format=None):
        offset = request.query_params.get('offset', 0)
        all_authors = tales_models.Author.objects.filter(pk__gt=offset)
        serializer = tales_serializers.AuthorSerializer(all_authors, many=True)
        return Response(
            {
                'state': 'Success',
                'error': 0,
                'authors': serializer.data
            }
        )

class GetTalesOfAuthor(APIView):

    def get(self, request, *args, **kwargs):
        author_id =  self.kwargs.get("author_id", None)
        if author_id is not None:
            try:
                author = tales_models.Author.objects.get(pk=author_id)
                tales = tales_models.Tale.objects.filter(author=author)
                serializer = tales_serializers.TaleSerializer(tales, many=True)
                return Response(
                    {
                        'state': 'Success',
                        'error': 0,
                        'tales': serializer.data
                    }
                )
            except tales_models.Author.DoesNotExist:
                return Response(
                {
                    'state': 'Author does not exists',
                    'error': 1
                }
            )
        else:
            return Response(
                {
                    'state': 'No author id sended',
                    'error': 1
                }
            )

class GetSentencesOfTale(APIView):

    def get(self, request, *args, **kwargs):

        tale_id =  self.kwargs.get("tale_id", None)
        if tale_id is not None:
            try:
                tale = tales_models.Tale.objects.get(pk=tale_id)
                sentences = tales_models.TaleSentence.objects.filter(tale=tale)
                serializer = tales_serializers.TaleSentenceSerializer(sentences, many=True)
                return Response(
                    {
                        'state': 'Success',
                        'error': 0,
                        'sentences': serializer.data
                    }
                )
            except tales_models.Tale.DoesNotExist:
                return Response(
                {
                    'state': 'Tale does not exists',
                    'error': 1
                }
            )
        else:
            return Response(
                {
                    'state': 'No tale id sended',
                    'error': 1
                }
            )

class VoteTale(APIView):

    def post(self, request, format=None):
        serializer = tales_serializers.TaleVoteSerializer(data=request.data)
        if serializer.is_valid(True):
            print(serializer.validated_data)
            tale = serializer.validated_data['tale']
            tale.calification = (tale.calification * tale.total_votes + serializer.validated_data['calification'])/\
                                (tale.total_votes+1)
            tale.total_votes += 1
            tale.save()
            serializer.save()

            return Response(
                {
                    'state': 'Success',
                    'error': 0,
                    'data': serializer.data
                }
            )
        else:
            return Response(
                {
                    'state': 'Failure',
                    'error': 1
                }
            )


class GetRandomSentence(APIView):

    def get(self, request, format=None):
        print(tales_models.TaleSentence.objects.count())
        random_tale = random.random()*tales_models.Tale.objects.count()
        tale_sentences = tales_models.TaleSentence.objects.filter(tale__id=random_tale)
        random_sentence_id = tale_sentences[0].id
        sentence = tales_models.TaleSentence.objects.get(pk=random_sentence_id)
        serializer = tales_serializers.TaleSentenceSerializer(sentence)

        return Response(serializer.data)

class GetNextSentence(APIView):

    def get(self, request, format=None):
        print(tales_models.TaleSentence.objects.count())
        print(request.query_params)
        random_tale = random.random()*tales_models.Tale.objects.count()
        tale_sentences = tales_models.TaleSentence.objects.filter(tale__id=random_tale)
        random_sentence_id = tale_sentences[0].id
        sentence = tales_models.TaleSentence.objects.get(
            pk=(int)(request.query_params.get(
                'id',
                random_sentence_id
            ))+1
        )
        serializer = tales_serializers.TaleSentenceSerializer(sentence)

        return Response(serializer.data)

class RankingTable(APIView):

    def get(self, request, format=None):
        count_datas = core_models.AnonymousAudioData.objects.values('user').annotate(
            user_count=models.Count('user')
        ).order_by('-user_count')
        for count_data in count_datas:
            count_data['user'] = authentication_models.AnonymousUserProfile.objects.get(pk=count_data['user']).anonymous_name
        print(count_datas)
        return Response(count_datas)

class DownloadMostReadedTales(APIView):

    def get(self, request, format=None):
        offset = request.query_params.get('offset', 50)
        sentence_tales = tales_models.SentenceTaleSpeech.objects.values('tale_sentence').annotate(
            count=models.Count('tale_sentence')
        ).order_by('-count')[:offset]

        audio_datas = []
        print(sentence_tales)
        for s in sentence_tales:
            speech_tales = tales_models.SentenceTaleSpeech.objects.filter(tale_sentence__id=s['tale_sentence'])
            for a in speech_tales:
                audio_datas.append(
                    a.audio
                )

        serializer = core_serializers.AudioDataSerializer(audio_datas, many=True)
        return Response(serializer.data)
