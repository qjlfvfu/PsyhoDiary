import os
from celery import Celery
from celery.schedules import crontab

# Устанавливаем модуль настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Загружаем настройки из Django settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находим задачи в приложениях
app.autodiscover_tasks()

# Расписание периодических задач (Celery Beat)
app.conf.beat_schedule = {
    # Проверка пропущенных лекарств каждый час
    "check-missed-medications-hourly": {
        "task": "pillowtracker.tasks.check_missed_medications",
        "schedule": crontab(minute=0),  # каждый час
    },
    # Проверка низкого настроения каждые 3 часа
    "check-low-mood-every-3-hours": {
        "task": "pillowtracker.tasks.check_low_mood",
        "schedule": crontab(minute=0, hour="*/3"),  # каждые 3 часа
    },
    # Отправка ежедневной статистики врачам в 9 утра
    "send-daily-stats-to-doctors": {
        "task": "users.tasks.send_daily_stats_to_doctors",
        "schedule": crontab(hour=9, minute=0),
    },
    # Очистка логов в 3 ночи
    "cleanup-old-logs": {
        "task": "utils.tasks.cleanup_old_logs",
        "schedule": crontab(hour=3, minute=0),
    },
    # Деактивация статуса активности для пользователей с 4го дня
    "deactivate-inactive-users-daily": {
        "task": "users.tasks.deactivate_inactive_users",
        "schedule": crontab(hour=2, minute=0),  # каждый день в 2 часа ночи
        "args": (4,),  # деактивировать после 4 дней неактивности
    },
}

if __name__ == "__main__":
    app.start()
