from rest_framework import views as rest_framework_views
from rest_framework import response

from . import serializers as news_serializers
from . import models as news_models
class AllNews(rest_framework_views.APIView):

    def get(self, request, format=None):
        offset = request.query_params.get('offset', 0)
        all_news = news_models.New.objects.filter(pk__gt=offset)
        serializer = news_serializers.NewSerializer(all_news, many=True)
        return response.Response(serializer.data)
