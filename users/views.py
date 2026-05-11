from django.shortcuts import redirect, render, get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.decorators import login_required, user_passes_test
from pillowtracker.models import MedicationLog, Alert
from psyhodiary.models import Diary, Dream, EmergencyContact, Habit
from .serializers import (
    MyTokenObtainPairSerializer,
    UserDetailSerializer,
    UserSerializer,
    UserCreateSerializer,
)
from .models import CustomUser
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, DoctorRegistrationForm

User = CustomUser


class MyTokenObtainPairView(TokenObtainPairView):
    """Получение Токена"""
    serializer_class = MyTokenObtainPairSerializer

# =============== Регистрация ===============

class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

# Отдельная регистрация для врачей
class DoctorRegisterView(CreateView):
    form_class = DoctorRegistrationForm
    template_name = 'users/doctor_register.html'
    success_url = reverse_lazy('users:login')


# =============== CRUD User (API) ===============

class UserListAPIView(generics.ListAPIView):
    """Список пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр пользователя"""
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Доктора, модераторы и админы видят всех
        if user.is_staff or user.groups.filter(name="moderators").exists() or user.groups.filter(
                name="doctor").exists():
            return User.objects.all()

        # Обычный пользователь видит только себя
        return User.objects.filter(id=user.id)

    def get_object(self):
        if self.kwargs.get("pk") == "me":
            return self.request.user
        return super().get_object()


class UserCreateAPIView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED
        )


class UserUpdateAPIView(generics.UpdateAPIView):
    """Обновление информации о пользователе"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserDestroyAPIView(generics.DestroyAPIView):
    """Удаление пользователя"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Администраторы и модераторы могут удалять любого
        if user.is_staff or user.groups.filter(name="moderators").exists():
            return User.objects.all()
        # Обычный пользователь может удалить только себя
        return User.objects.filter(id=user.id)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Пользователь удален"},
            status=status.HTTP_204_NO_CONTENT,
        )


# =============== HTML представления (для профиля) ===============

class ProfileView(LoginRequiredMixin, DetailView):
    """Профиль пользователя (HTML)"""
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля (HTML)"""
    model = CustomUser
    template_name = 'users/profile_edit.html'
    fields = ['first_name', 'last_name', 'avatar', 'phone_number']
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлён!')
        return super().form_valid(form)

# ==================== ПОМОЩЬ И ЭКСТРЕННЫЕ КОНТАКТЫ ====================
def help_page(request):
    """Страница помощи"""
    contacts = EmergencyContact.objects.all()
    return render(request, 'users/help.html', {'contacts': contacts})


def emergency_help(request):
    """Страница экстренной помощи"""
    contacts = EmergencyContact.objects.filter(is_24h=True)
    return render(request, 'users/emergency_help.html', {'contacts': contacts})


# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================
def check_user_mood(user):
    """Проверяет настроение пользователя и отправляет предупреждение"""
    if Diary.check_low_mood(user, days=3, threshold=7):
        # Сообщение пользователю
        messages.warning(
            user,
            "⚠️ Ваше настроение последние 3 дня низкое. Рекомендуем обратиться к специалисту."
        )

        # Логирование
        print(f"[ALERT] Пользователь {user.email}: низкое настроение")

        return True
    return False
# ==================== ФУНКЦИИ ДЛЯ ВРАЧЕЙ ====================
def is_doctor(user):
    return user.is_doctor or user.is_staff


@login_required
@user_passes_test(is_doctor)
def doctor_patients(request):
    doctor_profile = request.user.doctor_profile
    patients = CustomUser.objects.filter(attending_doctor=doctor_profile)

    # Поиск
    query = request.GET.get('q', '')
    if query:
        patients = patients.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(name__icontains=query)
        )

    return render(request, 'doctors/patients_list.html', {
        'patients': patients,
        'query': query
    })


@login_required
@user_passes_test(is_doctor)
def add_patient(request):
    doctor_profile = request.user.doctor_profile

    # Получаем пользователей, которые ещё не привязаны к этому врачу
    existing_patients = CustomUser.objects.filter(attending_doctor=doctor_profile)

    # Исключаем уже привязанных, а также самого врача
    available_users = CustomUser.objects.filter(
        is_doctor=False,
        is_staff=False,
        is_superuser=False
    ).exclude(
        id__in=existing_patients.values_list('id', flat=True)
    ).exclude(
        id=request.user.id
    )

    # Поиск
    query = request.GET.get('q', '')  # ← пустая строка по умолчанию
    if query:
        available_users = available_users.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    return render(request, 'doctors/add_patient.html', {
        'available_users': available_users,
        'query': query
    })

@login_required
@user_passes_test(is_doctor)
def assign_patient(request, user_id):
    doctor_profile = request.user.doctor_profile

    # Нельзя назначить себя
    if user_id == request.user.id:
        messages.error(request, 'Вы не можете добавить самого себя как пациента')
        return redirect('users:add_patient')

    patient = get_object_or_404(CustomUser, id=user_id)

    # Проверяем, что пользователь не врач и не админ
    if patient.is_doctor or patient.is_staff:
        messages.error(request, 'Нельзя назначить врача или администратора как пациента')
        return redirect('users:add_patient')

    # Проверяем, не привязан ли уже
    if patient.attending_doctor:
        messages.warning(request, f'Пользователь {patient.email} уже привязан к другому врачу')
    else:
        patient.attending_doctor = doctor_profile
        patient.save()
        messages.success(request, f'Пациент {patient.email} успешно добавлен')

    return redirect('users:patients_list')


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(CustomUser, pk=pk)

    # Проверяем доступ врача
    if request.user.is_doctor:
        doctor_profile = request.user.doctor_profile
        if patient.attending_doctor != doctor_profile:
            messages.error(request, 'У вас нет доступа к этому пациенту')
            return redirect('users:patients_list')

    # Считаем статистику
    diary_count = Diary.objects.filter(user=patient).count()
    dreams_count = Dream.objects.filter(user=patient).count()
    habits_count = Habit.objects.filter(user=patient).count()
    medication_count = MedicationLog.objects.filter(user=patient).count()

    # Последняя активность (используем поле last_active из модели)
    last_active = patient.last_active
    if last_active:
        last_active_formatted = last_active.strftime("%d.%m.%Y %H:%M")
    else:
        last_active_formatted = "нет данных"

    return render(request, 'doctors/patient_detail.html', {
        'patient': patient,
        'diary_count': diary_count,
        'dreams_count': dreams_count,
        'habits_count': habits_count,
        'medication_count': medication_count,
        'last_active': last_active_formatted,
    })


@login_required
@user_passes_test(is_doctor)
def doctor_alerts(request):
    alerts = Alert.objects.filter(doctor=request.user).order_by('-created_at')
    return render(request, 'doctors/alerts.html', {'alerts': alerts})


@login_required
@user_passes_test(is_doctor)
def mark_alert_read(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id, doctor=request.user)
    alert.is_read = True
    alert.save()
    messages.success(request, 'Оповещение отмечено как прочитанное')

    # Возвращаемся на предыдущую страницу
    next_url = request.GET.get('next', 'users:doctor_alerts')
    return redirect(next_url)