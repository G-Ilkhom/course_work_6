from django.db import models

from users.models import User


class Client(models.Model):
    email = models.EmailField(null=True, blank=True)
    full_name = models.CharField(max_length=100)
    comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')

    def __str__(self):
        return self.full_name


class Message(models.Model):
    topic = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.topic


class Mailing(models.Model):
    DAYLY = 'Раз в день'
    WEEKLY = 'Раз в неделю'
    MONTHLY = 'Раз в месяц'

    SENDING_PERIOD = [
        (DAYLY, 'Раз в день'),
        (WEEKLY, 'Раз в неделю'),
        (MONTHLY, 'Раз в месяц'),
    ]

    CREATED = 'Создана'
    STARTED = 'Запущена'
    FINISHED = 'Завершена'

    SELECT_STATUS = [
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
        (FINISHED, 'Завершена'),
    ]

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    frequency = models.CharField(max_length=20, choices=SENDING_PERIOD)
    status = models.CharField(default=CREATED, max_length=20, choices=SELECT_STATUS)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    client = models.ManyToManyField(Client)
    is_disabled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.start_date}-{self.end_date}, {self.frequency}, {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('disable_mailing', 'Может отключать рассылки'),
        ]


class MailingAttempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='ссылка на рассылку')
    attempt_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    server_response = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'

    def __str__(self):
        return f'Попытка рассылки от {self.attempt_date} ({self.status})'
