from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Medication, MedicationLog

User = get_user_model()


class MedicationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com", name="Test", password="test123"
        )

    def test_create_medication(self):
        med = Medication.objects.create(
            user=self.user, name="Aspirin", dosage="500mg", schedule_time="08:00"
        )
        self.assertEqual(med.name, "Aspirin")

    def test_medication_log(self):
        med = Medication.objects.create(
            user=self.user, name="Aspirin", dosage="500mg", schedule_time="08:00"
        )
        log = MedicationLog.objects.create(medication=med, user=self.user, taken=True)
        self.assertTrue(log.taken)
