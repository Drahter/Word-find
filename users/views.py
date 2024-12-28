import secrets

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView

from users.forms import UserRegisterForm
from users.models import User

from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    """Контроллер для регистрации новых пользователей"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Валидация электронной почты через отправку письма с подтверждением"""
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save(update_fields=['token', 'is_active'])
        host = self.request.get_host()
        url = f'/http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Для подтверждения регистрации перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    ordering = ['pk']


def email_verification(request, token):
    """Функция для активации пользователя после перехода по ссылке из письма"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def reset_password(request):
    """Функия для смены пароля пользователем, присылает случайный на указанную почту"""
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()

        send_mail(
            subject='Восстановление пароля',
            message=f'Вы запрашивали обновление пароля. Ваш новый пароль: {password}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        render(request, 'users/reset_password.html')
        return redirect(reverse("users:login"))

    return render(request, 'users/reset_password.html')


@login_required
def user_activity(request, pk):
    """Функция для смены активности пользователей(не получателей)"""
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    elif not user.is_active:
        user.is_active = True
    user.save()

    return redirect(reverse('users:user_list'))
