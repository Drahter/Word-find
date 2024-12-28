from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Создание суперюзера"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@gmail.com',
            first_name='Администратор',
            last_name='Системы',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('12345q')
        user.save()
