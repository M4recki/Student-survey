from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(  # type: ignore
            email="test@example.com",
            password="oldpassword123",
            first_name="Test",
            last_name="User",
        )

    def test_password_reset_request_view(self):
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "password_reset_form.html")

    def test_password_reset_email_sent(self):
        response = self.client.post(
            reverse("password_reset"), {"email": self.user.email}
        )
        self.assertRedirects(response, reverse("password_reset_done"))

    def test_password_reset_confirm_view(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "password_reset_confirm.html")
