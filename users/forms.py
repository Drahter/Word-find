from django.contrib.auth.forms import UserCreationForm

from django.forms import BooleanField, widgets
from users.models import User


class StyleFormMixin:
    """Миксин для стандартизации форм"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            if isinstance(field.widget, widgets.DateTimeInput):
                field.widget.input_type = 'datetime-local'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
