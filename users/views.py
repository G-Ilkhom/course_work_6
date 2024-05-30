import secrets
import string
import logging
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from users.models import User
from users.forms import UserRegisterForm
from django.urls import reverse_lazy, reverse
from config.settings import EMAIL_HOST_USER
from django.shortcuts import redirect, render
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.contrib import messages


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:email_verification')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'

        try:
            send_mail(
                subject="Подтверждение почты",
                message=f"Привет, перейди по ссылке для подтверждения почты {url}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            logging.info(f"Email sent to {user.email}")
        except Exception as e:
            logging.error(f"Error sending email to {user.email}: {e}")

        return super().form_valid(form)


def email_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                token = secrets.token_hex(16)
                user.token = token
                user.save()

                host = request.get_host()
                url = f'http://{host}/users/email-confirm/{token}/'

                try:
                    send_mail(
                        subject="Подтверждение почты",
                        message=f"Привет, перейди по ссылке для подтверждения почты {url}",
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[user.email]
                    )
                    logging.info(f"Email sent to {user.email}")
                    return redirect('users:successfully')
                except Exception as e:
                    logging.error(f"Error sending email to {user.email}: {e}")
            else:
                messages.error(request, "Ваша учетная запись уже активирована.")
        except User.DoesNotExist:
            messages.error(request, "Пользователь с указанным email-адресом не найден.")
    return render(request, 'users/message_verification.html')


def email_confirm(request, token):
    try:
        user = User.objects.get(token=token)
        user.is_active = True
        user.token = ''
        user.save()
        return redirect(reverse("users:successfully"))
    except User.DoesNotExist:
        messages.error(request, "Пользователь с указанным токеном не найден.")
        return redirect(reverse("users:email_verification"))


def successfully(request):
    return render(request, 'users/successfully.html')


class UserPasswordResetView(PasswordResetView):
    template_name = 'recovery_form.html'
    success_url = reverse_lazy('users:login')

    def post(self, request):
        email = request.POST.get('email')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            user.set_password(new_password)
            user.save()
            send_mail(
                subject="Восстановление пароля",
                message=f"Доброго времени суток!\n"
                        f"Ваш пароль для доступа на сайт AppleStore изменен.\n"
                        f"Данные для входа:\n"
                        f"Email: {email}\n"
                        f"Пароль: {new_password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            return HttpResponseRedirect(reverse('users:login'))
        except User.DoesNotExist:
            messages.error(request, "Пользователь с указанным email-адресом не найден.")
            return render(request, self.template_name)


@permission_required('users.block_users')
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


@permission_required('users.block_users')
def block_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_blocked = True
    user.save()
    return HttpResponseRedirect(reverse('users:user_list'))


@permission_required('users.block_users')
def unblock_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_blocked = False
    user.save()
    return HttpResponseRedirect(reverse('users:user_list'))
