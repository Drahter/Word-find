from django.contrib import admin

from finder.models import Article


@admin.register(Article)
class AdminRegisterArticle(admin.ModelAdmin):
    """Отображение статей в панели администрирования"""
    list_filter = ('id', 'rubrics', 'created_date')
