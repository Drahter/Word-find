from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from finder.models import Article
from finder.search import ArticleIndex


class ArticleAPITestCase(APITestCase):
    def setUp(self):
        self.article = Article.objects.create(rubrics=['Тестовая', 'статья'], text='Текст для тестовой статьи')

    def test_article_retrieve(self):
        url = reverse('finder_api:api_article_detail', args=(self.article.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('rubrics'), ['Тестовая', 'статья']
        )
        self.assertEqual(
            data.get('id'), 1
        )

    def test_elasticsearch_api_get_results(self):
        url = reverse('finder_api:api_search')
        response = self.client.post(url, {'query': 'текст'}, format='json')
        results = response.data

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(len(results), 1)

        self.assertEqual(
            results[0]['rubrics'], 'Тестовая, статья'
        )

    def clear(self):
        ArticleIndex.get(id=self.article.pk).delete()
        print("Document deleted")  # Логирование удаления
