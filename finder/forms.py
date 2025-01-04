from django.forms import ModelForm
from django.core.exceptions import ValidationError

from finder.models import Document
from users.forms import StyleFormMixin


class DocumentForm(ModelForm, StyleFormMixin):
    class Meta:
        model = Document
        fields = '__all__'

    def clean_text(self):
        """Функции для контроля содержимого документов"""
        cleaned_data = self.cleaned_data.get('text')

        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for each in forbidden_words:
            if each in cleaned_data:
                raise ValidationError('Извините, такое содержание недопустимо для статьи')

        return cleaned_data
