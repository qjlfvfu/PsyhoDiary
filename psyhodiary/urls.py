from django.urls import path
from . import views

app_name = 'psyhodiary'

urlpatterns = [
    # Главная
    path('', views.main_page, name='main'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Дневник
    path('diary/', views.diary_list, name='diary_list'),
    path('diary/create/', views.diary_create, name='diary_create'),
    path('diary/<int:pk>/', views.diary_detail, name='diary_detail'),
    path('diary/<int:pk>/update/', views.diary_update, name='diary_update'),
    path('diary/<int:pk>/delete/', views.diary_delete, name='diary_delete'),

    # Мечты
    path('dreams/', views.dream_list, name='dream_list'),
    path('dreams/create/', views.dream_create, name='dream_create'),
    path('dreams/<int:pk>/update/', views.dream_update, name='dream_update'),
    path('dreams/<int:pk>/delete/', views.dream_delete, name='dream_delete'),

    # Трекер привычек
    path('habits/', views.habit_list, name='habit_list'),
    path('habits/create/', views.habit_create, name='habit_create'),
    path('habits/<int:pk>/log/', views.habit_log, name='habit_log'),

    # Тесты
    path('tests/', views.test_list, name='test_list'),
    path('tests/<slug:test_slug>/', views.test_take, name='test_take'),
    path('tests/results/', views.test_results, name='test_results'),

]