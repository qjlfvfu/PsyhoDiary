from celery import shared_task


@shared_task
def check_daily_reminders():
    # логика для дневника
    pass


@shared_task
def check_medication_tracker():
    # логика для трекера таблеток
    pass
