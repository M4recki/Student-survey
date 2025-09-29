from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Survey

User = get_user_model()


class SurveyCreationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user( # type: ignore
            email="creator@example.com",
            password="securepass123",
            first_name="Test",
            last_name="Student",
        )
        self.create_url = reverse("create_survey")

    def test_create_survey_requires_login(self):
        response = self.client.get(self.create_url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.create_url}")

    def test_create_survey_success(self):
        self.client.login(email=self.user.email, password="securepass123")
        response = self.client.post(
            self.create_url,
            {
                "title": "Student Satisfaction Survey",
                "description": "Help us improve your experience.",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Survey.objects.filter(title="Student Satisfaction Survey").exists()
        )

    def test_create_survey_missing_title(self):
        self.client.login(email=self.user.email, password="securepass123")
        response = self.client.post(
            self.create_url, {"title": "", "description": "Missing title test"}
        )
        self.assertContains(response, "Survey title is required.")
