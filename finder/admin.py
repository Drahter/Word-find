from django.contrib import admin

from finder.models import Article


@admin.register(Article)
class AdminRegisterUser(admin.ModelAdmin):
    list_filter = ('id', 'rubrics', 'created_date')
