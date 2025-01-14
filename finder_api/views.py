from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from finder.models import Article
from finder_api.serializers import ArticleSerializer, SearchSerializer
from finder_api.services import api_get_results


# Create your views here.
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class APISearchView(APIView):
    def post(self, request):
        serializer = SearchSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']

            results = api_get_results(query)

            return Response(results, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
