from django.forms import ModelForm, Form, CharField, TextInput
from django.core.exceptions import ValidationError

from finder.models import Article
from users.forms import StyleFormMixin


class ArticleForm(ModelForm, StyleFormMixin):
    """Форма для модели Article, для единообразного отображения используется StyleFormMixin"""
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['owner']

    def clean_text(self):
        """Функция для контроля содержимого документов"""
        cleaned_data = self.cleaned_data.get('text')

        if not cleaned_data:
            raise ValidationError('Это поле обязательно для заполнения.')

        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for each in forbidden_words:
            if each in cleaned_data:
                raise ValidationError('Извините, такое содержание недопустимо для статьи')

        return cleaned_data


class SearchForm(Form):
    """Форма для поля поиска информации"""
    query = CharField(label='Введите текст запроса: ', max_length=50,
                      widget=TextInput(attrs={'placeholder': 'Поиск по тексту'}))

