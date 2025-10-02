from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Survey

User = get_user_model()


class SurveyListVisibilityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user( # type: ignore
            email="user@example.com", password="userpass123"
        )
        self.approved = Survey.objects.create(
            title="Approved",
            description="Visible",
            created_by=self.user,
            is_approved=True,
        )
        self.unapproved = Survey.objects.create(
            title="Hidden",
            description="Invisible",
            created_by=self.user,
            is_approved=False,
        )
        self.list_url = reverse("survey")

    def test_only_approved_surveys_visible(self):
        self.client.login(email=self.user.email, password="userpass123")
        response = self.client.get(self.list_url)
        self.assertContains(response, "Approved")
        self.assertNotContains(response, "Hidden")
