from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


# 1. Ежедневник (записи)
class Diary(models.Model):
    objects = None
    MOOD_CHOICES = [
        (1, "😞 Очень плохо"),
        (2, "😕 Плохо"),
        (3, "😐 Нормально"),
        (4, "🙂 Хорошо"),
        (5, "😊 Отлично"),
    ]

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    mood = models.IntegerField(
        choices=MOOD_CHOICES, default=3, verbose_name="Настроение"
    )
    created_date = models.DateField(auto_now_add=True, verbose_name="Дата")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="diary_entries"
    )

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "Запись дневника"
        verbose_name_plural = "Записи дневника"

    def __str__(self):
        return f"{self.title} - {self.created_date}"

    @classmethod
    def check_low_mood(cls, user, days=3, threshold=7):
        """Проверяет, не ниже ли сумма настроений за последние N дней порога"""
        start_date = timezone.now().date() - timedelta(days=days)
        entries = cls.objects.filter(user=user, created_date__gte=start_date)

        if entries.count() < days:
            return False

        total_mood = sum(entry.mood for entry in entries)
        return total_mood < threshold


# 2. Мечты (цели, желания)
class Dream(models.Model):
    STATUS_CHOICES = [
        ("draft", "Черновик"),
        ("in_progress", "В процессе"),
        ("completed", "Исполнено"),
        ("postponed", "Отложено"),
    ]

    title = models.CharField(max_length=150, verbose_name="Мечта / цель")
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="draft", verbose_name="Статус"
    )
    target_date = models.DateField(
        null=True, blank=True, verbose_name="Планируемая дата"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dreams"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Мечта"
        verbose_name_plural = "Мечты"

    def __str__(self):
        return self.title


# 3. Трекер привычек
class Habit(models.Model):
    PERIOD_CHOICES = [
        ("daily", "Ежедневно"),
        ("weekly", "Еженедельно"),
        ("monthly", "Ежемесячно"),
    ]

    name = models.CharField(max_length=100, verbose_name="Привычка")
    description = models.TextField(blank=True, verbose_name="Описание")
    period = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES,
        default="daily",
        verbose_name="Периодичность",
    )
    target_count = models.PositiveIntegerField(
        default=1, verbose_name="Цель (раз в период)"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits"
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return self.name


# 4. Отметки выполнения привычек
class HabitLog(models.Model):
    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, related_name="logs", verbose_name="Привычка"
    )
    completed_date = models.DateField(auto_now_add=True, verbose_name="Дата выполнения")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habit_logs"
    )

    class Meta:
        unique_together = ("habit", "completed_date", "user")
        verbose_name = "Отметка привычки"
        verbose_name_plural = "Отметки привычек"

    def __str__(self):
        return f"{self.habit.name} - {self.completed_date}"


# 5. Результаты тестов
class TestResult(models.Model):
    test_name = models.CharField(max_length=200, verbose_name="Название теста")
    score = models.IntegerField(verbose_name="Результат (баллы)")
    interpretation = models.TextField(blank=True, verbose_name="Интерпретация")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата прохождения"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="test_results"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"

    def __str__(self):
        return f"{self.test_name} - {self.score} баллов"


# 6. Экстренная помощь (контакты)
class EmergencyContact(models.Model):
    objects = None
    title = models.CharField(max_length=100, verbose_name="Название службы")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_24h = models.BooleanField(default=True, verbose_name="Круглосуточно")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Экстренный контакт"
        verbose_name_plural = "Экстренные контакты"

    def __str__(self):
        return f"{self.title} - {self.phone}"
