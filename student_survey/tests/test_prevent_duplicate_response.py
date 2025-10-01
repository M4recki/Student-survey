from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Survey, Question, Choice, Response, Answer

User = get_user_model()


class PreventDuplicateResponseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user( # type: ignore
            email="user@example.com", password="userpass123"
        )
        self.survey = Survey.objects.create(
            title="Feedback Survey",
            description="Tell us what you think",
            created_by=self.user,
            is_approved=True,
        )
        self.question = Question.objects.create(
            survey=self.survey, text="How was it?", question_type="radio"
        )
        self.choice = Choice.objects.create(question=self.question, text="Great")
        self.take_url = reverse("take_survey", args=[self.survey.id]) # type: ignore

    def test_user_can_submit_once(self):
        self.client.login(email=self.user.email, password="userpass123")
        response = self.client.post(
            self.take_url, {f"question_{self.question.id}": str(self.choice.id)} # type: ignore
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Response.objects.filter(survey=self.survey, user=self.user).exists()
        )

        # Try submitting again
        response = self.client.post(
            self.take_url,
            {f"question_{self.question.id}": str(self.choice.id)}, # type: ignore
            follow=True,
        )
        self.assertContains(response, "You have already completed this survey.")
