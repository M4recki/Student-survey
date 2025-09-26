from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTests(TestCase):
    def setUp(self):
        self.signup_url = reverse("signup")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.home_url = reverse("home")

        self.user_data = {
            "first_name": "test",
            "last_name": "test",
            "email": "marek@example.com",
            "password": "Secure123!",
            "confirm_password": "Secure123!",
        }

    def test_signup_success(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertRedirects(response, self.home_url)
        self.assertTrue(User.objects.filter(email=self.user_data["email"]).exists())

    def test_signup_password_mismatch(self):
        data = self.user_data.copy()
        data["confirm_password"] = "Wrong123!"
        response = self.client.post(self.signup_url, data)
        self.assertContains(response, "Passwords do not match.")

    def test_signup_short_password(self):
        data = self.user_data.copy()
        data["password"] = data["confirm_password"] = "short"
        response = self.client.post(self.signup_url, data)
        self.assertContains(response, "Password must be at least 8 characters long.")

    def test_login_success(self):
        User.objects.create_user( # type: ignore
            email=self.user_data["email"],
            password=self.user_data["password"],
            first_name="test",
            last_name="test",
        )
        response = self.client.post(
            self.login_url,
            {"email": self.user_data["email"], "password": self.user_data["password"]},
        )
        self.assertRedirects(response, self.home_url)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            self.login_url, {"email": "wrong@example.com", "password": "WrongPass123"}
        )
        self.assertContains(response, "Invalid email or password.")

    def test_remember_me_session_expiry(self):
        User.objects.create_user( # type: ignore
            email=self.user_data["email"],
            password=self.user_data["password"],
            first_name="test",
            last_name="test",
        )
        response = self.client.post(
            self.login_url,
            {
                "email": self.user_data["email"],
                "password": self.user_data["password"],
                "remember_me": "on",
            },
        )
        self.assertEqual(self.client.session.get_expiry_age(), 1209600)

    def test_logout(self):
        user = User.objects.create_user( # type: ignore
            email=self.user_data["email"],
            password=self.user_data["password"],
            first_name="test",
            last_name="test",
        )
        self.client.login(email=user.email, password=self.user_data["password"])
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)
