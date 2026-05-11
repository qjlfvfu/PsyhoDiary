from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Medication, MedicationLog, Alert
from psyhodiary.models import Diary


@shared_task
def check_missed_medications():
    """Проверяет пропущенные лекарства"""
    today = timezone.now().date()
    current_time = timezone.now().time()

    # Лекарства, которые нужно было принять в последние 2 часа
    two_hours_ago = (timezone.now() - timedelta(hours=2)).time()

    medications = Medication.objects.filter(
        is_active=True,
        schedule_time__lte=current_time,
        schedule_time__gte=two_hours_ago,
        start_date__lte=today,
    )

    created_alerts = 0

    for med in medications:
        log_exists = MedicationLog.objects.filter(
            medication=med, user=med.user, taken_at__date=today
        ).exists()

        if not log_exists and med.user.attending_doctor:
            doctor = med.user.attending_doctor.user

            Alert.objects.create(
                user=med.user,
                doctor=doctor,
                alert_type="missed_medication",
                message=f"Пациент {med.user.email} пропустил приём '{med.name}' в {med.schedule_time}",
            )

            send_mail(
                subject=f"⚠️ Пропуск лекарства - {med.user.email}",
                message=f"Пациент {med.user.email} не отметил приём {med.name} в {med.schedule_time}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[doctor.email],
                fail_silently=True,
            )
            created_alerts += 1

    return (
        f"Проверено {medications.count()} лекарств, создано {created_alerts} оповещений"
    )


@shared_task
def check_low_mood():
    """Проверяет низкое настроение у пациентов"""
    today = timezone.now().date()
    three_days_ago = today - timedelta(days=3)

    from users.models import DoctorProfile

    doctors = DoctorProfile.objects.all()
    created_alerts = 0

    for doctor_profile in doctors:
        for patient in doctor_profile.patients.all():
            entries = Diary.objects.filter(
                user=patient, created_date__gte=three_days_ago
            ).order_by("created_date")[:3]

            if entries.count() == 3:
                total_mood = sum(e.mood for e in entries)

                if total_mood < 7:
                    alert_exists = Alert.objects.filter(
                        user=patient,
                        doctor=doctor_profile.user,
                        alert_type="low_mood",
                        created_at__date=today,
                    ).exists()

                    if not alert_exists:
                        Alert.objects.create(
                            user=patient,
                            doctor=doctor_profile.user,
                            alert_type="low_mood",
                            message=f"У пациента {patient.email} низкое настроение (сумма за 3 дня: {total_mood}/15)",
                        )

                        send_mail(
                            subject=f"⚠️ Низкое настроение - {patient.email}",
                            message=f"За последние 3 дня у пациента {patient.email} низкий эмоциональный фон.\n\nСумма баллов: {total_mood}/15.\n\nРекомендуется связаться с пациентом.",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[doctor_profile.user.email],
                            fail_silently=True,
                        )
                        created_alerts += 1

    return f"Проверено {doctors.count()} врачей, создано {created_alerts} оповещений"


@shared_task
def test_task(message):
    """Тестовая задача"""
    print(f"Тестовая задача выполнена: {message}")
    return f"Готово: {message}"
