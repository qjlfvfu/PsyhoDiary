from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import DoctorProfile

User = get_user_model()

class UserRegistrationTest(TestCase):
    def test_patient_registration(self):
        response = self.client.post(reverse('users:register'), {
            'email': 'patient@test.com',
            'name': 'Test Patient',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)  # redirect after success
        self.assertTrue(User.objects.filter(email='patient@test.com').exists())

    def test_doctor_registration(self):
        response = self.client.post(reverse('users:doctor_register'), {
            'email': 'doctor@test.com',
            'name': 'Test Doctor',
            'specialization': 'Psychiatrist',
            'experience_years': 5,
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='doctor@test.com')
        self.assertTrue(user.is_doctor)
        self.assertTrue(DoctorProfile.objects.filter(user=user).exists())


class DoctorPatientTest(TestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(
            email='doctor@test.com',
            name='Doctor',
            password='testpass123',
            is_doctor=True
        )
        self.doctor_profile = DoctorProfile.objects.create(user=self.doctor)
        self.patient = User.objects.create_user(
            email='patient@test.com',
            name='Patient',
            password='testpass123'
        )

    def test_doctor_can_add_patient(self):
        self.client.login(email='doctor@test.com', password='testpass123')
        response = self.client.post(reverse('users:assign_patient', args=[self.patient.id]))
        self.assertEqual(response.status_code, 302)
        self.patient.refresh_from_db()
        self.assertEqual(self.patient.attending_doctor, self.doctor_profile)