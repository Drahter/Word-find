from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from finder.documents import ArticleDocument
from finder.models import Article
from finder.services import save_article_doc
from users.models import User


class ArticleAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.article = Article.objects.create(owner=self.user, rubrics=['Тестовая', 'статья'], text='Текст для тестовой статьи')
        save_article_doc(self.article)

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
