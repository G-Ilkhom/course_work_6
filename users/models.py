from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class UserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name="Имя пользователя")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=35, verbose_name="Телефон", blank=True, null=True,
                             help_text="Введите номер телефона")
    country = models.CharField(max_length=35, verbose_name="Страна", blank=True, null=True,
                               help_text="Введите страну")
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True,
                               help_text="Загрузите свой аватар")
    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокирован")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    object = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ('block_users', 'Может блокировать пользователей сервиса'),
        ]

    def __str__(self):
        return self.email
