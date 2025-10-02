from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Survey, Question, Choice, Response, Answer

User = get_user_model()


class AdminStatsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user( # type: ignore
            email="admin@example.com",
            password="adminpass123",
            first_name="Admin",
            last_name="User",
            is_superuser=True,
            is_staff=True,
        )
        self.user = User.objects.create_user( # type: ignore
            email="user@example.com", password="userpass123"
        )
        self.survey = Survey.objects.create(
            title="Satisfaction Survey",
            description="Rate your experience",
            created_by=self.admin,
            is_approved=True,
        )
        self.question = Question.objects.create(
            survey=self.survey, text="How satisfied are you?", question_type="radio"
        )
        self.choice = Choice.objects.create(
            question=self.question, text="Very satisfied"
        )
        self.response = Response.objects.create(survey=self.survey, user=self.user)
        self.answer = Answer.objects.create(
            response=self.response, question=self.question, choice=self.choice
        )
        self.stats_url = reverse("admin_stats")

    def test_admin_stats_requires_login(self):
        response = self.client.get(self.stats_url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.stats_url}")

    def test_admin_stats_requires_superuser(self):
        self.client.login(email=self.user.email, password="userpass123")
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, 302)

    def test_admin_stats_shows_response_count(self):
        self.client.login(email=self.admin.email, password="adminpass123")
        response = self.client.get(self.stats_url)
        self.assertContains(response, "Satisfaction Survey")

        # Check if the response count is displayed 
        self.assertContains(response, "<p class=\"stat-value\">1</p>")

    def test_superuser_sees_stats(self):
        self.client.login(email="admin@example.com", password="adminpass123")
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Total Surveys")
        self.assertContains(response, "Total Responses")
        self.assertContains(response, "Avg. Response Rate")