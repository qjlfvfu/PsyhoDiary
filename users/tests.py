from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import DoctorProfile
from pillowtracker.models import Alert

User = get_user_model()


class UserRegistrationTest(TestCase):
    def test_patient_registration(self):
        response = self.client.post(
            reverse("users:register"),
            {
                "email": "patient@test.com",
                "name": "Test Patient",
                "last_name": "Patientov",
                "phone_number": "+79991234567",
                "description": "Test description",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="patient@test.com").exists())

    def test_doctor_registration(self):
        response = self.client.post(
            reverse("users:register_doctor"),
            {
                "email": "doctor@test.com",
                "name": "Test Doctor",
                "last_name": "Doktorov",
                "phone_number": "+79991234567",
                "description": "Doctor description",
                "specialization": "Psychiatrist",
                "experience_years": 5,
                "license_number": "LIC123456",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email="doctor@test.com")
        self.assertTrue(user.is_doctor)
        self.assertTrue(DoctorProfile.objects.filter(user=user).exists())


class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            name="Test User",
            last_name="Userov",
            password="testpass123",
        )

    def test_login_page(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(
            reverse("users:login"),
            {"username": "test@test.com", "password": "testpass123"},
        )
        self.assertEqual(response.status_code, 302)  # redirect after login


class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            name="Test User",
            last_name="Userov",
            password="testpass123",
        )
        self.client.login(email="test@test.com", password="testpass123")

    def test_profile_page(self):
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_page(self):
        response = self.client.get(reverse("users:profile_edit"))
        self.assertEqual(response.status_code, 200)


class DoctorPatientTest(TestCase):
    def setUp(self):
        # Создаём врача
        self.doctor = User.objects.create_user(
            email="doctor@test.com",
            name="Test Doctor",
            last_name="Doktorov",
            password="testpass123",
            is_doctor=True,
        )
        self.doctor_profile = DoctorProfile.objects.create(user=self.doctor)

        # Создаём пациента
        self.patient = User.objects.create_user(
            email="patient@test.com",
            name="Test Patient",
            last_name="Patientov",
            password="testpass123",
        )

        self.client.login(email="doctor@test.com", password="testpass123")

    def test_patients_list(self):
        response = self.client.get(reverse("users:patients_list"))
        self.assertEqual(response.status_code, 200)

    def test_add_patient_page(self):
        response = self.client.get(reverse("users:add_patient"))
        self.assertEqual(response.status_code, 200)

    def test_assign_patient(self):
        response = self.client.post(
            reverse("users:assign_patient", args=[self.patient.id])
        )
        self.assertEqual(response.status_code, 302)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.attending_doctor, self.doctor_profile)

    def test_patient_detail(self):
        # Сначала назначаем пациента
        self.patient.attending_doctor = self.doctor_profile
        self.patient.save()

        response = self.client.get(
            reverse("users:patient_detail", args=[self.patient.id])
        )
        self.assertEqual(response.status_code, 200)


class DoctorAlertsTest(TestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(
            email="doctor@test.com",
            name="Test Doctor",
            last_name="Doktorov",
            password="testpass123",
            is_doctor=True,
        )
        self.doctor_profile = DoctorProfile.objects.create(user=self.doctor)

        self.patient = User.objects.create_user(
            email="patient@test.com",
            name="Test Patient",
            last_name="Patientov",
            password="testpass123",
            attending_doctor=self.doctor_profile,
        )

        self.alert = Alert.objects.create(
            user=self.patient,
            doctor=self.doctor,
            alert_type="low_mood",
            message="Test alert message",
        )

        self.client.login(email="doctor@test.com", password="testpass123")

    def test_alerts_list(self):
        response = self.client.get(reverse("users:doctor_alerts"))
        self.assertEqual(response.status_code, 200)

    def test_mark_alert_read(self):
        response = self.client.get(
            reverse("users:mark_alert_read", args=[self.alert.id])
        )
        self.assertEqual(response.status_code, 302)
        self.alert.refresh_from_db()
        self.assertTrue(self.alert.is_read)


class HelpPagesTest(TestCase):
    def test_help_page(self):
        response = self.client.get(reverse("users:help"))
        self.assertEqual(response.status_code, 200)

    def test_emergency_help_page(self):
        response = self.client.get(reverse("users:emergency_help"))
        self.assertEqual(response.status_code, 200)


class ApiViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            name="Test User",
            last_name="Userov",
            password="testpass123",
        )

    def test_api_token(self):
        response = self.client.post(
            reverse("users:token_obtain_pair"),
            {"email": "test@test.com", "password": "testpass123"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.json())

    def test_api_user_create(self):
        response = self.client.post(
            reverse("users:user_create"),
            {
                "email": "new@test.com",
                "password": "testpass123",
                "password2": "testpass123",
                "first_name": "New",
                "last_name": "User",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email="new@test.com").exists())

    def test_api_user_list_requires_auth(self):
        response = self.client.get(reverse("users:user_list"))
        self.assertEqual(response.status_code, 401)  # Unauthorized
