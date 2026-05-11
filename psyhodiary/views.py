from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from users.views import check_user_mood
from .forms import DiaryForm, DreamForm, HabitForm
from .models import Diary, Dream, Habit, HabitLog, TestResult


# ==================== ДИАДЖЕСТ (ГЛАВНАЯ) ====================
@login_required
def dashboard(request):
    """Главная страница с графиком настроения"""
    from datetime import timedelta

    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)

    entries = Diary.objects.filter(
        user=request.user, created_date__range=[start_date, end_date]
    ).order_by("created_date")

    labels = [e.created_date.strftime("%d.%m") for e in entries]
    moods = [e.mood for e in entries]

    # Статистика
    total_entries = Diary.objects.filter(user=request.user).count()
    total_dreams = Dream.objects.filter(user=request.user).count()
    total_habits = Habit.objects.filter(user=request.user).count()

    context = {
        "labels": labels,
        "moods": moods,
        "total_entries": total_entries,
        "total_dreams": total_dreams,
        "total_habits": total_habits,
    }
    return render(request, "psyhodiary/dashboard.html", context)


# ==================== ДНЕВНИК (CRUD) ====================
@login_required
def diary_list(request):
    """Список записей дневника с пагинацией"""
    entries_list = Diary.objects.filter(user=request.user).order_by("-created_date")

    paginator = Paginator(entries_list, 10)  # 10 записей на страницу

    page = request.GET.get("page")
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)

    return render(request, "psyhodiary/diary_list.html", {"diary_entries": entries})


@login_required
def diary_create(request):
    """Создание записи"""
    if request.method == "POST":
        form = DiaryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()

            # Проверка настроения
            check_user_mood(request.user)

            messages.success(request, "Запись сохранена!")
            return redirect("psyhodiary:diary_detail", pk=entry.pk)
    else:
        form = DiaryForm()

    return render(request, "psyhodiary/diary_form.html", {"form": form})


@login_required
def diary_detail(request, pk):
    """Детальный просмотр записи"""
    entry = get_object_or_404(Diary, pk=pk, user=request.user)
    return render(request, "psyhodiary/diary_detail.html", {"diary_entry": entry})


@login_required
def diary_update(request, pk):
    """Редактирование записи"""
    entry = get_object_or_404(Diary, pk=pk, user=request.user)
    if request.method == "POST":
        form = DiaryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()

            # Проверка настроения после обновления
            check_user_mood(request.user)

            messages.success(request, "Запись обновлена!")
            return redirect("psyhodiary:diary_detail", pk=entry.pk)
    else:
        form = DiaryForm(instance=entry)

    return render(request, "psyhodiary/diary_form.html", {"form": form})


@login_required
def diary_delete(request, pk):
    """Удаление записи"""
    entry = get_object_or_404(Diary, pk=pk, user=request.user)
    if request.method == "POST":
        entry.delete()
        messages.success(request, "Запись удалена!")
        return redirect("psyhodiary:diary_list")

    return render(
        request, "psyhodiary/diary_confirm_delete.html", {"diary_entry": entry}
    )


# ==================== МЕЧТЫ (CRUD) ====================
@login_required
def dream_list(request):
    """Список мечт с пагинацией"""
    dreams_list = Dream.objects.filter(user=request.user).order_by("-created_at")

    paginator = Paginator(dreams_list, 10)

    page = request.GET.get("page")
    try:
        dreams = paginator.page(page)
    except PageNotAnInteger:
        dreams = paginator.page(1)
    except EmptyPage:
        dreams = paginator.page(paginator.num_pages)

    return render(request, "psyhodiary/dream_list.html", {"dreams": dreams})


@login_required
def dream_create(request):
    """Создание мечты"""
    if request.method == "POST":
        form = DreamForm(request.POST)
        if form.is_valid():
            dream = form.save(commit=False)
            dream.user = request.user
            dream.save()
            messages.success(request, "Мечта добавлена!")
            return redirect("psyhodiary:dream_list")
    else:
        form = DreamForm()

    return render(request, "psyhodiary/dream_form.html", {"form": form})


@login_required
def dream_update(request, pk):
    """Редактирование мечты"""
    dream = get_object_or_404(Dream, pk=pk, user=request.user)
    if request.method == "POST":
        form = DreamForm(request.POST, instance=dream)
        if form.is_valid():
            form.save()
            messages.success(request, "Мечта обновлена!")
            return redirect("psyhodiary:dream_list")
    else:
        form = DreamForm(instance=dream)

    return render(request, "psyhodiary/dream_form.html", {"form": form})


@login_required
def dream_delete(request, pk):
    """Удаление мечты"""
    dream = get_object_or_404(Dream, pk=pk, user=request.user)
    if request.method == "POST":
        dream.delete()
        messages.success(request, "Мечта удалена!")
        return redirect("psyhodiary:dream_list")

    return render(request, "psyhodiary/dream_confirm_delete.html", {"dream": dream})


# ==================== ТРЕКЕР ПРИВЫЧЕК ====================
@login_required
def habit_list(request):
    """Список привычек с пагинацией"""
    habits_list = Habit.objects.filter(user=request.user).order_by("name")

    paginator = Paginator(habits_list, 10)

    page = request.GET.get("page")
    try:
        habits = paginator.page(page)
    except PageNotAnInteger:
        habits = paginator.page(1)
    except EmptyPage:
        habits = paginator.page(paginator.num_pages)

    return render(request, "psyhodiary/habit_list.html", {"habits": habits})


@login_required
def habit_create(request):
    """Создание привычки"""
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, "Привычка добавлена!")
            return redirect("psyhodiary:habit_list")
    else:
        form = HabitForm()

    return render(request, "psyhodiary/habit_form.html", {"form": form})


@login_required
def habit_log(request, pk):
    """Отметить выполнение привычки сегодня"""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()

    # Проверяем, не отмечали ли уже сегодня
    existing_log = HabitLog.objects.filter(
        habit=habit, user=request.user, completed_date=today
    ).first()

    if request.method == "POST":
        if not existing_log:
            HabitLog.objects.create(
                habit=habit, user=request.user, completed_date=today
            )
            messages.success(
                request, f'Привычка "{habit.name}" отмечена как выполненная!'
            )
        else:
            messages.warning(request, "Вы уже отмечали эту привычку сегодня!")
        return redirect("psyhodiary:habit_list")

    return render(
        request,
        "psyhodiary/habit_log.html",
        {"habit": habit, "already_logged": existing_log is not None},
    )


# ==================== ТЕСТЫ ====================
@login_required
def test_list(request):
    """Список доступных тестов"""
    return render(request, "psyhodiary/test_list.html")


@login_required
def test_take(request, test_slug):
    """Прохождение теста"""
    # Здесь будет логика теста (вопросы и ответы)
    # Пока заглушка
    if request.method == "POST":
        score = int(request.POST.get("score", 0))
        TestResult.objects.create(
            test_name=test_slug,
            score=score,
            interpretation="Интерпретация результата",
            user=request.user,
        )
        messages.success(request, "Тест пройден!")
        return redirect("psyhodiary:test_results")

    return render(request, "psyhodiary/test_take.html", {"test_slug": test_slug})


@login_required
def test_results(request):
    """Список пройденных тестов с пагинацией"""
    results_list = TestResult.objects.filter(user=request.user).order_by(
        "-completed_at"
    )

    paginator = Paginator(results_list, 10)

    page = request.GET.get("page")
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(request, "psyhodiary/test_results.html", {"results": results})


# ==================== СТАТИЧЕСКИЕ СТРАНИЦЫ ====================
def main_page(request):
    context = {}

    if request.user.is_authenticated and request.user.is_doctor:
        from pillowtracker.models import Alert, MedicationLog
        from django.utils import timezone

        try:
            doctor_profile = request.user.doctor_profile
            patients = doctor_profile.patients.all()
            context["patients_count"] = patients.count()
            context["unread_alerts_count"] = Alert.objects.filter(
                doctor=request.user, is_read=False
            ).count()
            context["today_missed"] = MedicationLog.objects.filter(
                user__in=patients, taken=False, taken_at__date=timezone.now().date()
            ).count()
        except:
            context["patients_count"] = 0
            context["unread_alerts_count"] = 0
            context["today_missed"] = 0

    return render(request, "psyhodiary/main.html", context)
