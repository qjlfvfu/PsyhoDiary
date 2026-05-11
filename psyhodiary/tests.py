from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.utils import timezone

from .models import Diary

User = get_user_model()


class DiaryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com", name="Test", password="test123"
        )

    def test_create_diary_entry(self):
        entry = Diary.objects.create(
            title="My day", content="Today was good", mood=4, user=self.user
        )
        self.assertEqual(entry.title, "My day")
        self.assertEqual(entry.mood, 4)

    def test_low_mood_check(self):
        for i in range(3):
            Diary.objects.create(
                title=f"Day {i}",
                content="Sad",
                mood=2,
                user=self.user,
                created_date=timezone.now().date() - timedelta(days=i),
            )
        self.assertTrue(Diary.check_low_mood(self.user, days=3, threshold=7))
