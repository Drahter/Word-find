from django.shortcuts import render
from rest_framework import generics

from finder.models import Article
from finder_api.serializers import ArticleSerializer


# Create your views here.
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


