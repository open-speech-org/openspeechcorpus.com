import random

from rest_framework import views
from rest_framework import response

from . import serializers as miscellany_serializers
from . import models as miscellany_models
from applications.tales import models as tales_models
from applications.tales import serializers as tales_serializers
from applications.authentication import models as authentication_models

class CommandsView(views.APIView):

    def get(self, request, format=None):

        offset = int(request.query_params.get('offset', 0))
        commands = miscellany_models.Command.objects.all()[offset:offset+10]
        commands_serializer = miscellany_serializers.CommandSerializer(commands, many=True)

        print commands_serializer.data

        if request.query_params.get('new_user', False):
            print "New user requested"
            anonymous_user = authentication_models.AnonymousUserProfile(
                anonymous_name='anonymous_'+unicode(authentication_models.AnonymousUserProfile.objects.all().count())
            )
            anonymous_user.save()
            print anonymous_user
            anonymous_user_command_serialized = miscellany_serializers.AnonymousCommandSerializer(
                data={
                    'anonymous_user': anonymous_user.id,
                    'commands': commands_serializer.data
                }
            )
            print anonymous_user_command_serialized.is_valid()
            print anonymous_user_command_serialized.data
            return response.Response(anonymous_user_command_serialized.data)
        else:

            return response.Response(commands_serializer.data)

class UploadCommand(views.APIView):

    def post(self, request, format=None):

        print request.data
        audio_upload_tale_data = miscellany_serializers.CommandUploadSerializer(data=request.data)

        if audio_upload_tale_data.is_valid(True):
            print("True")
            audio_upload_tale_data.save()
            return response.Response(
                {
                    'state': 'Success',
                    'error': 0
                }
                )
        else:
            print("False")
            return response.Response(
                {
                    'state': 'Failure',
                    'error': 1
                }
            )