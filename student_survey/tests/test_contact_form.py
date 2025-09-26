from django.test import TestCase
from django.urls import reverse


class ContactFormTests(TestCase):
    def test_contact_form_view_get(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")

    def test_contact_form_submission(self):
        data = {
            "name": "Marek",
            "email": "marek@example.com",
            "subject": "Test Subject",
            "message": "Test message content",
        }
        response = self.client.post(reverse("about"), data)
        self.assertRedirects(response, reverse("about"))
