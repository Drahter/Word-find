from django.forms import ModelForm, Form, CharField, TextInput
from django.core.exceptions import ValidationError

from finder.models import Article
from users.forms import StyleFormMixin


class ArticleForm(ModelForm, StyleFormMixin):
    class Meta:
        model = Article
        fields = '__all__'

    def clean_text(self):
        """Функции для контроля содержимого документов"""
        cleaned_data = self.cleaned_data.get('text')

        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for each in forbidden_words:
            if each in cleaned_data:
                raise ValidationError('Извините, такое содержание недопустимо для документа')

        return cleaned_data


class SearchForm(Form):
    query = CharField(label='Введите текст запроса: ', max_length=50,
                      widget=TextInput(attrs={'placeholder': 'Поиск по тексту'}))

