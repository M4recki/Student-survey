from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Survey

User = get_user_model()

class SurveyDeletionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email="admin@example.com", password="adminpass") # type: ignore
        self.survey = Survey.objects.create(title="To Delete", description="Remove me", created_by=self.admin, is_approved=True)
        self.list_url = reverse("survey")

    def test_admin_can_delete_survey(self):
        self.client.login(email=self.admin.email, password="adminpass")
        response = self.client.post(self.list_url, {"survey_id": self.survey.id, "action": "delete"}, follow=True) # type: ignore
        self.assertNotContains(response, "To Delete")
        self.assertFalse(Survey.objects.filter(id=self.survey.id).exists()) # type: ignore
