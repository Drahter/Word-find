from django.test import TestCase
from django.urls import reverse

from finder.forms import ArticleForm
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


class ArticleFormTest(TestCase):
    def test_form_valid(self):
        form_data = {
            'rubrics': ['Test', 'Article'],
            'text': 'This is a test article text.'
        }
        form = ArticleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_title(self):
        form_data = {
            'rubrics': ['Test', 'Article'],
            'content': ''
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

    def test_form_invalid_text(self):
        form_data = {
            'rubrics': ['Test', 'Article'],
            'content': 'Казино'
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)


class ArticleViewTest(TestCase):
    def setUp(self):
        # Создаем пользователя и несколько статей для тестирования
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='testpass')

        self.article1 = Article.objects.create(rubrics=['Статья', 'Один'], text='Текст статьи 1', owner=self.user)
        self.article2 = Article.objects.create(rubrics=['Статья', 'Два'], text='Текст статьи 2', owner=self.user)
        self.article3 = Article.objects.create(rubrics=['Статья', 'Три'], text='Текст статьи 3', owner=self.user)

    def test_article_list_view_authenticated_user(self):
        self.client.login(email='testuser@test.com', password='testpass')

        response = self.client.get(reverse('finder:article_list'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Текст статьи 1')
        self.assertContains(response, 'Текст статьи 2')
        self.assertContains(response, 'Текст статьи 3')

    def test_article_list_view_unauthenticated_user(self):
        response = self.client.get(reverse('finder:article_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/' + '?next=/articles/')

    def test_article_create_view(self):
        self.client.login(email='testuser@test.com', password='testpass')

        url = reverse('finder:article_create')
        data = {
            'rubrics': ['Статья', 'Новая'],
            'text': 'Это новая статья.',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Article.objects.filter(text='Это новая статья.').exists())

        article = Article.objects.get(text='Это новая статья.')
        self.assertEqual(article.owner, self.user)

    def test_article_delete_view(self):
        self.client.login(email='testuser@test.com', password='testpass')
        # Создаем статью для удаления
        obj_to_delete = Article.objects.create(rubrics=[], text='Текст статьи для удаления', owner=self.user)

        # Убедитесь, что статья существует до удаления
        self.assertTrue(Article.objects.filter(pk=obj_to_delete.pk).exists())

        # Выполняем POST-запрос на удаление
        response = self.client.post(reverse('finder:article_delete', args=[obj_to_delete.pk]))

        # Проверяем статус ответа
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление

        # Проверяем, что статья была удалена
        self.assertFalse(Article.objects.filter(pk=obj_to_delete.pk).exists())  # Проверка на отсутствие


