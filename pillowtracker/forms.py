from django import forms
from .models import Medication, MedicationLog

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'schedule_time', 'days', 'start_date', 'end_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'schedule_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567 (1=ПН, 7=ВС)'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MedicationLogForm(forms.ModelForm):
    class Meta:
        model = MedicationLog
        fields = ['taken', 'skipped_reason']
        widgets = {
            'taken': forms.Select(attrs={'class': 'form-select'}, choices=[(True, '✅ Принято'), (False, '❌ Пропущено')]),
            'skipped_reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Причина пропуска (если не приняли)'}),
        }