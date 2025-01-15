from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.shortcuts import render, redirect
from elasticsearch import NotFoundError
from django.contrib.auth.mixins import LoginRequiredMixin
from elasticsearch_dsl import Search
from django.db.models.signals import post_delete
from django.dispatch import receiver

from finder.forms import ArticleForm, SearchForm
from finder.models import Article
from finder.services import get_results, save_article_doc
from users.models import User
from .documents import ArticleDocument


class ArticleListView(LoginRequiredMixin, ListView):
    """
       View to display a list of articles.

       This view retrieves all articles from the database and renders them
       using the specified template.

       Attributes:
           model (Article): The Article model to use for querying.
           template_name (str): The template to render.
    """
    model = Article

    def get_queryset(self):
        """Получить статьи для текущего пользователя"""
        return Article.objects.filter(owner=self.request.user)
        # def get_queryset(self):
    #     """Реализовано кэширование отдельных документов"""
    #     return get_documents_from_cache()


class ArticleDetailView(DetailView):
    model = Article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("finder:index")

    def form_valid(self, form):
        """Установка создающего пользователя как владельца"""
        article = form.save()
        user = self.request.user
        article.owner = user
        article.save()

        save_article_doc(article)

        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
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
        article = form.save()
        save_article_doc(article)

        return super().form_valid(form)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("finder:index")
    print('0')
    def post(self, request, *args, **kwargs):
        print('1')
        # Получаем объект для удаления
        self.object = self.get_object()
        id_for_delete = self.object.pk
        print(id_for_delete)

        # Удаляем объект из базы данных
        self.object.delete()
        print('2')
        # Удаляем документ из Elasticsearch
        try:
            # article = Article.objects.get(id=id_for_delete)
            # doc = Search(index='articles').query('match', id=id_for_delete)
            # doc.delete()
            article_document = ArticleDocument.get(id=id_for_delete)
            print(article_document)
            article_document.delete()
            print("Document deleted")
        except NotFoundError:
            print("Document not found in Elasticsearch")

        # Перенаправление на success_url
        return redirect(self.success_url)


class IndexView(TemplateView):
    template_name = 'finder/index.html'

    def get_context_data(self, **kwargs):
        """Получение данных из ДБ о количестве статей, пользователей и случайных статей"""
        context = super().get_context_data(**kwargs)

        context['total_articles'] = Article.objects.count()
        context['total_users'] = User.objects.count()
        context['random_articles'] = Article.objects.order_by('?')[:3]
        return context


class SearchView(FormView):
    template_name = 'finder/search_request.html'
    form_class = SearchForm

    def form_valid(self, form):
        user_input = form.cleaned_data['query']
        search_result = get_results(user_input)
        return render(self.request, 'finder/search_results.html', {'search_result': search_result})


class SearchResultsView(TemplateView):
    template_name = 'finder/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_result'] = self.kwargs.get('search_result')
        return context
