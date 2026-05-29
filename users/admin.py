from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, DoctorProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "name", "is_doctor", "is_active", "date_joined")
    list_filter = ("is_doctor", "is_active", "is_staff")
    search_fields = ("email", "name", "phone_number")
    ordering = ("-date_joined",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Личная информация",
            {"fields": ("name", "avatar", "phone_number", "description")},
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_doctor",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Медицинские данные", {"fields": ("attending_doctor",)}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2"),
            },
        ),
    )


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "specialization", "experience_years", "license_number")
    search_fields = ("user__email", "specialization")
