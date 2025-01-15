from django.test import TestCase

from finder.models import Article
from users.models import User


class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpass')
        self.client.login(email='testuser@test.com', password='testpass')
        self.article = Article.objects.create(
            rubrics=['Test', 'Article'],
            text='This is a test article.',
            owner=self.user
        )

    def test_article_creation(self):
        self.assertEqual(self.article.rubrics, ['Test', 'Article'])
        self.assertEqual(self.article.text, 'This is a test article.')
        self.assertEqual(self.article.owner.email, 'testuser@test.com')

    def test_article_update(self):
        self.article.rubrics = ['Updated', 'Test']
        self.article.text = 'This is an updated test article.'
        self.article.save()

        self.assertEqual(self.article.rubrics, ['Updated', 'Test'])
        self.assertEqual(self.article.text, 'This is an updated test article.')

    def test_article_deletion(self):
        self.article.delete()
        self.assertEqual(Article.objects.filter(id=self.article.id).exists(), False)
