from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from online_store.accounts.models import UserProfile


class ProfileViewsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(email="test@example.com", password="test_password")
        self.user_profile = UserProfile.objects.update(user=self.user, first_name="Test", last_name="User",
                                                       phone_number="1234567890", city="Test City",
                                                       address="Test Address")

        self.user2 = get_user_model().objects.create(email="test2@example.com", password="test_password2")

    def test_profile_edit_view_with_login_user(self):
        self.client.force_login(self.user)
        url = reverse("profile_edit", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_view_with_login_user_with_another_user(self):
        self.client.force_login(self.user)
        url = reverse("profile_edit", kwargs={"pk": self.user2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You do not have permission to edit this profile.")

    def test_profile_edit_view_change_phone_number(self):
        self.client.force_login(self.user)
        url = reverse("profile_edit", kwargs={"pk": self.user.pk})
        response = self.client.post(url, {"first_name": "Updated", "last_name": "User", "phone_number": "12345678901",
                                          "city": "Test City", "address": "Test Address"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ensure this value has at most 10 characters (it has 11).")

    def test_profile_edit_view_without_login_user(self):
        url = reverse("profile_edit", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.url, f"/login/?next=/accounts/edit/{self.user.pk}/")

    def test_profile_details_view(self):
        self.client.force_login(self.user)
        url = reverse("profile_details", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_details_view_without_login_user(self):
        url = reverse("profile_details", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/login/?next=/accounts/details/{self.user.pk}/")

    def test_profile_delete_view(self):
        self.client.force_login(self.user)
        url = reverse("profile_delete", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_delete_view_with_another_user(self):
        self.client.force_login(self.user)
        url = reverse("profile_delete", kwargs={"pk": self.user2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unauthorized access")

    def test_profile_details_view_with_another_user(self):
        self.client.force_login(self.user)
        url = reverse("profile_details", kwargs={"pk": self.user2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unauthorized access")

    def test_change_password_view(self):
        self.client.force_login(self.user)
        url = reverse("change_password", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
