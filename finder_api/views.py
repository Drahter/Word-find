from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from finder.models import Article
from finder_api.serializers import ArticleSerializer, SearchSerializer
from finder_api.services import api_get_results


# Create your views here.
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для получения информации об отдельной статье"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class APISearchView(APIView):
    """Контроллер для обработки запросов к Elasticsearch

    Принимает запрос с ключом 'query' и возвращает результаты поиска в формате списка словарей с данными о статьях
    """
    def get(self, request):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']

            results = api_get_results(query)

            return Response(results, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
