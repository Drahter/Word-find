from django.urls import path
from django.views.decorators.cache import cache_page

from finder.apps import FinderConfig
from finder.views import (
    DocumentListView,
    DocumentCreateView,
    DocumentDetailView,
    DocumentUpdateView,
    DocumentDeleteView,
    IndexView,
)

app_name = FinderConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('documents/', DocumentListView.as_view(),
         name='document_list'),
    path('documents/create/', DocumentCreateView.as_view(),
         name='document_create'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(),
         name='document_detail'),
    path('documents/<int:pk>/update/', DocumentUpdateView.as_view(),
         name='document_update'),
    path('documents/<int:pk>/delete/', DocumentDeleteView.as_view(),
         name='document_delete'),
]
