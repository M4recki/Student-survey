from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Survey, Question, Choice, Response, Answer

User = get_user_model()


class TakeSurveyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user( # type: ignore
            email="student@example.com",
            password="studentpass123",
            first_name="Test",
            last_name="Student",
        )
        self.survey = Survey.objects.create(
            title="Feedback Survey",
            description="Let us know your thoughts",
            created_by=self.user,
            is_approved=True,
        )
        self.question = Question.objects.create(
            survey=self.survey, text="How satisfied are you?", question_type="radio"
        )
        self.choice1 = Choice.objects.create(
            question=self.question, text="Very satisfied"
        )
        self.choice2 = Choice.objects.create(
            question=self.question, text="Not satisfied"
        )
        self.take_url = reverse("take_survey", args=[self.survey.id]) # type: ignore

    def test_take_survey_requires_login(self):
        response = self.client.get(self.take_url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.take_url}")

    def test_take_survey_view(self):
        self.client.login(email=self.user.email, password="studentpass123")
        response = self.client.get(self.take_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.text)

    def test_submit_survey_response(self):
        self.client.login(email=self.user.email, password="studentpass123")
        response = self.client.post(
            self.take_url, {f"question_{self.question.id}": str(self.choice1.id)} # type: ignore
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Response.objects.filter(survey=self.survey, user=self.user).exists()
        )
        self.assertTrue(
            Answer.objects.filter(question=self.question, choice=self.choice1).exists()
        )
