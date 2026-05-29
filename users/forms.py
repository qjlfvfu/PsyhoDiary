from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, DoctorProfile


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(required=True, label="Имя")
    email = forms.EmailField(required=True)
    last_name = forms.CharField(required=True, label="Фамилия")
    phone_number = forms.CharField(required=False, label="Телефон")
    description = forms.CharField(widget=forms.Textarea, required=False, label="О себе")

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "phone_number", "description"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"].split("@")[0]
        if commit:
            user.save()
        return user


class DoctorRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True, label="Имя")
    last_name = forms.CharField(required=True, label="Фамилия")
    phone_number = forms.CharField(required=False, label="Телефон")
    description = forms.CharField(widget=forms.Textarea, required=False, label="О себе")

    # Поля для профиля врача
    specialization = forms.CharField(
        max_length=200, required=False, label="Специализация"
    )
    experience_years = forms.IntegerField(
        min_value=0, required=False, label="Лет опыта"
    )
    license_number = forms.CharField(
        max_length=50, required=False, label="Номер лицензии"
    )

    class Meta:
        model = CustomUser
        fields = ["email", "name", "last_name", "phone_number", "description"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"].split("@")[0]
        user.is_doctor = True
        if commit:
            user.save()
            # Создаём профиль врача
            DoctorProfile.objects.create(
                user=user,
                specialization=self.cleaned_data.get("specialization", ""),
                experience_years=self.cleaned_data.get("experience_years", 0),
                license_number=self.cleaned_data.get("license_number", ""),
            )
        return user
