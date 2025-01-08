from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.shortcuts import render, redirect

from finder.forms import DocumentForm, SearchForm
from finder.models import Document
from users.models import User


class DocumentListView(ListView):
    model = Document

    # def get_queryset(self):
    #     """Реализовано кэширование отдельных документов"""
    #     return get_documents_from_cache()


class DocumentDetailView(DetailView):
    model = Document


class DocumentCreateView(CreateView):
    model = Document
    form_class = DocumentForm
    success_url = reverse_lazy("finder:document_list")


class DocumentUpdateView(UpdateView):
    model = Document
    form_class = DocumentForm
    success_url = reverse_lazy("finder:document_list")


class DocumentDeleteView(DeleteView):
    model = Document
    success_url = reverse_lazy("finder:document_list")


class IndexView(TemplateView):
    template_name = 'finder/index.html'

    def get_context_data(self, **kwargs):
        """Получение данных из ДБ о количестве документов, пользователей и случайных документов"""
        context = super().get_context_data(**kwargs)

        context['total_documents'] = Document.objects.count()
        context['total_users'] = User.objects.count()
        context['random_docs'] = Document.objects.order_by('?')[:3]
        return context


class SearchView(FormView):
    template_name = 'finder/search_request.html'
    form_class = SearchForm

    def form_valid(self, form):
        user_input = form.cleaned_data['query']
        print(user_input)
#         return render(self.request, 'results.html', {'user_input': user_input})


class SearchResultsView(ListView):
    pass


class OutputView(TemplateView):
    template_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_input'] = self.kwargs.get('user_input')
        return context
