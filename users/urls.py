from tkinter.font import names
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


app_name = 'users'

urlpatterns = [
    # JWT токены (API)
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/', views.UserListAPIView.as_view(), name='user_list'),
    path('api/users/create/', views.UserCreateAPIView.as_view(), name='user_create'),
    path('api/users/<str:pk>/', views.UserRetrieveAPIView.as_view(), name='user_detail'),
    path('api/users/<int:pk>/update/', views.UserUpdateAPIView.as_view(), name='user_update'),
    path('api/users/<int:pk>/delete/', views.UserDestroyAPIView.as_view(), name='user_delete'),

    # HTML представления
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('register/doctor/', views.DoctorRegisterView.as_view(), name='register_doctor'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('patients/', views.doctor_patients, name='patients_list'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/assign/<int:user_id>/', views.assign_patient, name='assign_patient'),
    path('alerts/', views.doctor_alerts, name='doctor_alerts'),
    path('alert/<int:alert_id>/read/', views.mark_alert_read, name='mark_alert_read'),
    # Помощь
    path('help/', views.help_page, name='help'),
    path('emergency/', views.emergency_help, name='emergency_help'),
]