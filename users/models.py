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

    email = models.EmailField(verbose_name="Почта",unique=True)
    avatar = models.ImageField(verbose_name="Аватарка",upload_to="avatars/", blank=True, null=True)
    description = models.TextField(verbose_name="Описание болезни",blank=True,null=False)
    phone_number = models.CharField(verbose_name="Номер телефона",max_length=15, blank=True, null=False)
    is_active = models.BooleanField(verbose_name="Активность пользователя",default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class CustomDoctor(AbstractUser):
    """Модель для Врачей"""

    email = models.EmailField(verbose_name="Почта",unique=True)
    avatar = models.ImageField(verbose_name="Аватар",upload_to="avatars/",blank=False,null=False)
    is_staff = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS =[]
