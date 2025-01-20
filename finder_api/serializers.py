from rest_framework import serializers

from finder.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Article"""
    class Meta:
        model = Article
        fields = '__all__'


class SearchSerializer(serializers.Serializer):
    """Сериалайзер для поисковых запросов"""
    query = serializers.CharField(required=True, max_length=50)
