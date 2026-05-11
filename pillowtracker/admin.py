from django.contrib import admin
from .models import Medication, MedicationLog, Alert


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "dosage", "schedule_time", "is_active")
    list_filter = ("is_active", "schedule_time")
    search_fields = ("name", "user__email")


@admin.register(MedicationLog)
class MedicationLogAdmin(admin.ModelAdmin):
    list_display = ("medication", "user", "taken_at", "taken")
    list_filter = ("taken", "taken_at")
    search_fields = ("medication__name", "user__email")


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("user", "doctor", "alert_type", "created_at", "is_read")
    list_filter = ("alert_type", "is_read", "created_at")
    search_fields = ("user__email", "doctor__email", "message")
