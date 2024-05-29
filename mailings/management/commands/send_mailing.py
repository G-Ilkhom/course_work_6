from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from django.core.mail import send_mail
from datetime import datetime, timedelta
import pytz
from django.conf import settings
from mailings.models import Mailing, MailingAttempt

period_mailing = ["Раз в день", "Раз в неделю", "Раз в месяц"]


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(status="Запущена")

    for mailing in mailings:

        if mailing.start_date <= current_datetime:
            status = False
            server_response = "Нет ответа"

            try:
                recipient_emails = [client.email for client in mailing.client.all()]
                send_mail(
                    subject=mailing.message.topic,
                    message=mailing.message.content,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=recipient_emails,
                    fail_silently=False
                )

                if mailing.frequency == period_mailing[0]:
                    mailing.start_date += timedelta(days=1)
                elif mailing.frequency == period_mailing[1]:
                    mailing.start_date += timedelta(weeks=1)
                elif mailing.frequency == period_mailing[2]:
                    mailing.start_date += timedelta(days=30)

                mailing.save()

                status = True
                server_response = "Успешно"

            except smtplib.SMTPResponseException as response:
                status = False
                server_response = str(response)

            finally:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status=status,
                    server_response=server_response,
                )


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=60)
    scheduler.start()
