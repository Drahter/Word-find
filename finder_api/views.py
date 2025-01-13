from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from finder.models import Article
from finder.search import ArticleIndex
from finder_api.serializers import ArticleSerializer, SearchSerializer


# Create your views here.
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class APISearchView(APIView):
    def post(self, request):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']

            search = ArticleIndex.search().query("multi_match", query=query, fields=['rubrics', 'text'])
            response = search.execute()

            results = [
                {
                    'id': hit.meta.id,
                    'rubrics': hit.rubrics,
                    'text': hit.text
                }
                for hit in response
            ]

            return Response(results, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
