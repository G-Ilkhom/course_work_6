from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from mailings.management.commands.send_mailing import send_mailing


class Command(BaseCommand):
    help = 'Starts the scheduled mailings'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_mailing, 'interval', seconds=60)
        # send_mailing()
        scheduler.start()
