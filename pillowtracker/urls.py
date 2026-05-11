from django.urls import path
from . import views

app_name = 'pillowtracker'

urlpatterns = [
    path('', views.medication_list, name='medication_list'),
    path('create/', views.medication_create, name='medication_create'),
    path('<int:pk>/update/', views.medication_update, name='medication_update'),
    path('<int:pk>/delete/', views.medication_delete, name='medication_delete'),
    path('<int:pk>/log/', views.medication_log, name='medication_log'),
]