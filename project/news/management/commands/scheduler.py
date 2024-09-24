from django.core.management.base import BaseCommand
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .tasks import email_weekly_update


class Command(BaseCommand):
    help = 'Starts the APScheduler to send weekly updates.'

    def handle(self, *args, **options):
        # Создаем планировщик задач
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        # Добавляем задачу в планировщик
        scheduler.add_job(
            email_weekly_update,
            trigger=IntervalTrigger(weeks=1),
            id='email_weekly_update',
            replace_existing=True
        )

        # Запускаем планировщик
        scheduler.start()

        self.stdout.write(self.style.SUCCESS('APScheduler started!'))

        # Останавливаем планировщик при завершении работы Django
        from apscheduler.schedulers import SchedulerNotRunningError
        from django.core.signals import request_finished

        def shutdown_scheduler(*args, **kwargs):
            try:
                scheduler.shutdown()
            except SchedulerNotRunningError:
                pass

        request_finished.connect(shutdown_scheduler)