from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser, DoctorProfile
from psyhodiary.models import Diary


@shared_task
def send_daily_stats_to_doctors():
    """Отправляет ежедневную статистику врачам"""
    yesterday = timezone.now().date() - timedelta(days=1)

    doctors = DoctorProfile.objects.all()
    sent_count = 0

    for doctor_profile in doctors:
        patients = doctor_profile.patients.all()

        total_entries = Diary.objects.filter(
            user__in=patients, created_date=yesterday
        ).count()

        low_mood_count = 0
        for patient in patients:
            if Diary.check_low_mood(patient, days=3, threshold=7):
                low_mood_count += 1

        if patients.exists():
            send_mail(
                subject=f"📊 Ежедневная статистика | {yesterday}",
                message=f"""
Здравствуйте, {doctor_profile.user.email}!

Статистика за вчера ({yesterday}):

📝 Всего записей в дневнике: {total_entries}
😟 Пациентов с низким настроением (3+ дня): {low_mood_count}
👥 Всего пациентов: {patients.count()}

---
PsyDiary Bot
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[doctor_profile.user.email],
                fail_silently=True,
            )
            sent_count += 1

    return f"Статистика отправлена {sent_count} врачам"


@shared_task
def deactivate_inactive_users(days=4):
    """Деактивирует пользователей, не заходивших более N дней"""
    threshold_date = timezone.now() - timedelta(days=days)

    inactive_users = CustomUser.objects.filter(
        is_active=True, last_active__lt=threshold_date
    )

    count = inactive_users.count()

    for user in inactive_users:
        user.is_active = False
        user.save(update_fields=["is_active"])

        # Опционально: отправить уведомление врачу
        if user.attending_doctor:
            from pillowtracker.models import Alert

            Alert.objects.create(
                user=user,
                doctor=user.attending_doctor.user,
                alert_type="inactive_patient",
                message=f"Пациент {user.email} неактивен более {days} дней",
            )

    return f"Деактивировано {count} пользователей"
