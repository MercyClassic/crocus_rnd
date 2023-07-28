from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        from ...main import bot_run

        bot_run()
