from rest_framework import serializers

from finder.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=50)
