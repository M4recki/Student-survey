from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
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
        self.reset_url = reverse("password_reset")
        self.reset_done_url = reverse("password_reset_done")
        self.login_url = reverse("login")

    def test_password_reset_form_view(self):
        response = self.client.get(self.reset_url)
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

    def test_password_reset_confirm_and_login(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})

        get_resp = self.client.get(url)
        self.assertEqual(get_resp.status_code, 302)
        set_password_url = get_resp.url  # type: ignore

        # The view will take the token from the session and save the new password (POST to URL without token)
        new_password = "newsecurepassword123"
        response = self.client.post(
            set_password_url,
            {"new_password1": new_password, "new_password2": new_password},
        )
        self.assertRedirects(response, reverse("password_reset_complete"))

        # Verify that the user can log in with the new password
        login_response = self.client.post(
            self.login_url, {"email": self.user.email, "password": new_password}
        )
        self.assertRedirects(login_response, reverse("home"))
