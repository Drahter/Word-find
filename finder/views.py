from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.shortcuts import render, redirect

from finder.forms import ArticleForm, SearchForm
from finder.models import Article
from finder.services import get_results
from users.models import User
from finder.search import ArticleIndex


class ArticleListView(ListView):
    model = Article

    # def get_queryset(self):
    #     """Реализовано кэширование отдельных документов"""
    #     return get_documents_from_cache()


class ArticleDetailView(DetailView):
    model = Article


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("finder:article_list")

    def form_valid(self, form):
        """Установка создающего пользователя как владельца"""
        article = form.save()
        user = self.request.user
        article.owner = user
        article.save()

        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy("finder:article_list")


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy("finder:index")

    def delete(self, request, *args, **kwargs):
        # Переопределяем поведение при удалении
        self.object = self.get_object()
        id_for_delete = self.object.pk
        self.object.delete()
        ArticleIndex.get(id=id_for_delete).delete()
        print("Document deleted")
        return redirect('finder:index')


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
