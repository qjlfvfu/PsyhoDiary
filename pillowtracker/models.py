from django.db import models
from django.conf import settings
from django.utils import timezone

class Medication(models.Model):
    """Лекарство / таблетка"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=200, verbose_name="Название")
    dosage = models.CharField(max_length=100, verbose_name="Дозировка", help_text="например: 500мг")
    schedule_time = models.TimeField(verbose_name="Время приёма")
    days = models.CharField(max_length=50, default="1234567", verbose_name="Дни приёма (1=ПН, 7=ВС)")
    start_date = models.DateField(default=timezone.now, verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['schedule_time']
        verbose_name = "Лекарство"
        verbose_name_plural = "Лекарства"

    def __str__(self):
        return f"{self.name} ({self.dosage}) - {self.schedule_time}"


class MedicationLog(models.Model):
    """Лог приёма таблеток"""
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    taken_at = models.DateTimeField(default=timezone.now, verbose_name="Время приёма")
    taken = models.BooleanField(default=True, verbose_name="Принято")
    skipped_reason = models.CharField(max_length=200, blank=True, verbose_name="Причина пропуска")

    class Meta:
        ordering = ['-taken_at']
        verbose_name = "Лог приёма"
        verbose_name_plural = "Логи приёма"
        unique_together = ['medication', 'user', 'taken_at']

    def __str__(self):
        status = "✅" if self.taken else "❌"
        return f"{status} {self.medication.name} - {self.taken_at.strftime('%d.%m.%Y %H:%M')}"


class Alert(models.Model):
    ALERT_TYPES = [
        ('missed_medication', 'Пропуск лекарства'),
        ('low_mood', 'Низкое настроение (3+ дня)'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alerts')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_alerts',
                               null=True)
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.user.email}"