from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from finder.forms import ArticleForm, SearchForm
from finder.models import Article
from finder.services import save_article_doc, delete_article_doc, get_search_results
from users.models import User

"""Контроллеры приложения"""


class ArticleListView(LoginRequiredMixin, ListView):
    """Вывод списка всех статей текущего пользователя"""
    model = Article

    def get_queryset(self):
        """Получить статьи для текущего пользователя"""
        return Article.objects.filter(owner=self.request.user)


class ArticleDetailView(DetailView):
    """Подробная информация об отдельной статье"""
    model = Article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Создание новой статьи"""
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("finder:index")

    def form_valid(self, form):
        """Установка создающего пользователя как владельца и создание документа в ElasticSearch"""
        article = form.save()
        user = self.request.user
        article.owner = user
        article.save()

        save_article_doc(article)  # создание документа в ElasticSearch

        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение статьи"""
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("finder:index")

    def get_form_class(self):
        """Изменение объектов закрыто от не-владельцев"""
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return ArticleForm
        raise PermissionDenied

    def form_valid(self, form):
        """Внесение изменений в документ ElasticSearch"""
        article = form.save()
        save_article_doc(article)

        return super().form_valid(form)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление статьи"""
    model = Article
    success_url = reverse_lazy("finder:index")

    def post(self, request, *args, **kwargs):
        """При удалении объекта удаляется соответствующий документ в ElasticSearch"""
        self.object = self.get_object()
        id_for_delete = self.object.pk  # Получаем объект для удаления

        self.object.delete()  # Удаляем объект из базы данных

        delete_article_doc(id_for_delete)  # Удаляем документ из Elasticsearch

        return redirect(self.success_url)


class IndexView(TemplateView):
    """Контоллер для главной страницы"""
    template_name = 'finder/index.html'

    def get_context_data(self, **kwargs):
        """Получение данных из ДБ о количестве статей, пользователей и случайных статей"""
        context = super().get_context_data(**kwargs)

        context['total_articles'] = Article.objects.count()
        context['total_users'] = User.objects.count()
        context['random_articles'] = Article.objects.order_by('?')[:3]
        return context


class SearchView(FormView):
    """Контроллер поискового запроса"""
    form_class = SearchForm

    def form_valid(self, form):
        """Получение введенного запроса и передача данных контроллеру вывода результатов"""
        user_input = form.cleaned_data['query']
        search_result = get_search_results(user_input)  # поиск в базе ElasticSearch
        return render(self.request, 'finder/search_results.html', {'search_result': search_result})


class SearchResultsView(TemplateView):
    """Контроллер отображения результатов поиска"""
    template_name = 'finder/search_results.html'

    def get_context_data(self, **kwargs):
        """Получение результатов поиска и передача их в шаблон"""
        context = super().get_context_data(**kwargs)
        context['search_result'] = self.kwargs.get('search_result')
        return context
