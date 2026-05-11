from django.contrib import admin
from .models import Diary, Dream, Habit, HabitLog, TestResult, EmergencyContact

@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'mood', 'created_date')
    list_filter = ('mood', 'created_date')
    search_fields = ('title', 'content', 'user__email')
    date_hierarchy = 'created_date'

@admin.register(Dream)
class DreamAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'target_date', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'user__email')

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'period', 'target_count')
    list_filter = ('period',)
    search_fields = ('name', 'user__email')

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('habit', 'user', 'completed_date')
    list_filter = ('completed_date',)
    search_fields = ('habit__name', 'user__email')

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'user', 'score', 'created_at')
    list_filter = ('test_name', 'created_at')
    search_fields = ('test_name', 'user__email')

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'is_24h', 'order')
    list_editable = ('order',)
    ordering = ('order',)