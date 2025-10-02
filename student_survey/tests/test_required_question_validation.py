from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from student_survey.models import Survey, Question, Choice, Response

User = get_user_model()

class RequiredQuestionValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user( # type: ignore
            email="user@example.com", password="userpass123"
        )
        self.survey = Survey.objects.create(
            title="Required Test",
            description="Test required fields",
            created_by=self.user,
            is_approved=True,
        )
        self.question = Question.objects.create(
            survey=self.survey, text="Rate us", question_type="radio"
        )
        Choice.objects.create(question=self.question, text="Good")
        self.take_url = reverse("take_survey", args=[self.survey.id]) # type: ignore

    def test_missing_required_answer(self):
        self.client.login(email=self.user.email, password="userpass123")
        response = self.client.post(self.take_url, {}, follow=True)
        self.assertContains(response, "Please answer all required questions.")
        self.assertFalse(
            Response.objects.filter(survey=self.survey, user=self.user).exists()
        )
