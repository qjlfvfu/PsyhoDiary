from django import forms
from .models import Diary, Dream, Habit, HabitLog, TestResult, EmergencyContact


class DiaryForm(forms.ModelForm):
    """Форма для записи в дневнике"""

    class Meta:
        model = Diary
        fields = ['title', 'content', 'mood']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Ваша запись...'}),
            'mood': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'mood': 'Настроение',
        }


class DreamForm(forms.ModelForm):
    """Форма для записи мечты/цели"""

    class Meta:
        model = Dream
        fields = ['title', 'description', 'status', 'target_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название мечты'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Описание...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'title': 'Мечта / цель',
            'description': 'Описание',
            'status': 'Статус',
            'target_date': 'Планируемая дата',
        }


class HabitForm(forms.ModelForm):
    """Форма для привычки"""

    class Meta:
        model = Habit
        fields = ['name', 'description', 'period', 'target_count']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название привычки'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание...'}),
            'period': forms.Select(attrs={'class': 'form-select'}),
            'target_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'name': 'Привычка',
            'description': 'Описание',
            'period': 'Периодичность',
            'target_count': 'Цель (раз в период)',
        }


class HabitLogForm(forms.ModelForm):
    """Форма для отметки выполнения привычки"""

    class Meta:
        model = HabitLog
        fields = []
        # Поля заполняются автоматически


class TestResultForm(forms.ModelForm):
    """Форма для результатов теста"""

    class Meta:
        model = TestResult
        fields = ['test_name', 'score', 'interpretation']
        widgets = {
            'test_name': forms.HiddenInput(),
            'score': forms.HiddenInput(),
            'interpretation': forms.HiddenInput(),
        }


class EmergencyContactForm(forms.ModelForm):
    """Форма для экстренных контактов (только для админа)"""

    class Meta:
        model = EmergencyContact
        fields = ['title', 'phone', 'description', 'is_24h', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_24h': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }