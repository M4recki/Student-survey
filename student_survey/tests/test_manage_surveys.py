from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from student_survey.models import Survey


User = get_user_model()


class ManageSurveysTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user( # type: ignore
            email="user@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

        self.superuser = User.objects.create_superuser( #type: ignore
            email="admin@example.com",
            password="adminpass123",
            first_name="Admin",
            last_name="User",
        )

        self.survey_user = Survey.objects.create(
            title="User Survey",
            description="Survey created by user",
            created_by=self.user,
            is_approved=False,
        )

        self.survey_super = Survey.objects.create(
            title="Owner's Survey",
            description="Survey created by superuser",
            created_by=self.superuser,
            is_approved=False,
        )
        self.manage_url = reverse("manage_surveys")

    def test_manage_surveys_requires_login(self):
        response = self.client.get(self.manage_url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.manage_url}")

    def test_manage_surveys_shows_all_for_superuser(self):
        self.client.login(email="admin@example.com", password="adminpass123")
        url = reverse("manage_surveys")
        response = self.client.get(url)

        self.assertContains(response, "User Survey")
        # Django escaping ' as &#x27;
        self.assertTrue(
            "Owner&#x27;s Survey" in response.content.decode()
            or "Owner's Survey" in response.content.decode(),
            "Superuser should see 2 surveys",
        )
