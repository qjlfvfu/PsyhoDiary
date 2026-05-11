from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextField


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Нужно добавить почту!!!")
        email = self.normalize_email(email)

        # АВТОМАТИЧЕСКИ СОЗДАЕМ USERNAME из email
        if "username" not in extra_fields or not extra_fields.get("username"):
            # Берем часть email до @ и убираем спецсимволы
            username = email.split("@")[0]
            # Убираем точки, дефисы и т.д.
            username = "".join(c for c in username if c.isalnum())
            if not username:
                username = f"user_{email[:8].replace('@', '')}"
            extra_fields["username"] = username

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Модель Пользователя"""
    name = models.CharField(max_length=150, verbose_name="Имя", blank=False, null=False)
    email = models.EmailField(verbose_name="Почта",unique=True)
    avatar = models.ImageField(verbose_name="Аватарка",upload_to="avatars/", blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="О себе")
    phone_number = models.CharField(verbose_name="Номер телефона",max_length=15, blank=True, null=False)
    is_active = models.BooleanField(verbose_name="Активность пользователя",default=True)
    is_staff = models.BooleanField(default=False)
    attending_doctor = models.ForeignKey(
        'DoctorProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patients',
        verbose_name="Лечащий врач"
    )
    is_doctor = models.BooleanField(default=False, verbose_name="Врач")
    last_active = models.DateTimeField(null=True, blank=True, verbose_name="Последняя активность")

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class DoctorProfile(models.Model):
    user = models.OneToOneField('users.CustomUser',on_delete=models.CASCADE,related_name='doctor_profile')
    specialization = models.CharField(max_length=200, blank=True, verbose_name="Специализация")
    experience_years = models.IntegerField(default=0, verbose_name="Лет опыта")
    license_number = models.CharField(max_length=50, blank=True, verbose_name="Номер лицензии")
    def __str__(self):
        return f"Доктор {self.user.email}"