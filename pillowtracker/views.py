from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Medication, MedicationLog
from .forms import MedicationForm, MedicationLogForm


@login_required
def medication_list(request):
    """Список лекарств пользователя"""
    medications = Medication.objects.filter(user=request.user, is_active=True)
    return render(request, 'pillowtracker/medication_list.html', {'medications': medications})


@login_required
def medication_create(request):
    """Добавить новое лекарство"""
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medication = form.save(commit=False)
            medication.user = request.user
            medication.save()
            messages.success(request, f'Лекарство "{medication.name}" добавлено!')
            return redirect('pillowtracker:medication_list')
    else:
        form = MedicationForm()
    return render(request, 'pillowtracker/medication_form.html', {'form': form})


@login_required
def medication_update(request, pk):
    """Редактировать лекарство"""
    medication = get_object_or_404(Medication, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            messages.success(request, f'Лекарство "{medication.name}" обновлено!')
            return redirect('pillowtracker:medication_list')
    else:
        form = MedicationForm(instance=medication)
    return render(request, 'pillowtracker/medication_form.html', {'form': form})


@login_required
def medication_delete(request, pk):
    """Удалить лекарство (деактивировать)"""
    medication = get_object_or_404(Medication, pk=pk, user=request.user)
    medication.is_active = False
    medication.save()
    messages.success(request, f'Лекарство "{medication.name}" удалено')
    return redirect('pillowtracker:medication_list')


@login_required
def medication_log(request, pk):
    """Отметить приём лекарства"""
    medication = get_object_or_404(Medication, pk=pk, user=request.user)

    if request.method == 'POST':
        form = MedicationLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.medication = medication
            log.user = request.user
            log.taken_at = timezone.now()
            log.save()
            messages.success(request, 'Приём отмечен!')
            return redirect('pillowtracker:medication_list')
    else:
        form = MedicationLogForm()

    return render(request, 'pillowtracker/medication_log.html', {
        'medication': medication,
        'form': form
    })
