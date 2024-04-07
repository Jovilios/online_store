from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from online_store.accounts.forms import CustomUserCreationForm, ProfileEditForm,ProfileDeleteForm
from online_store.accounts.models import UserProfile


class FormsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(email="test@example.com", password="Test123!")
        self.profile = UserProfile.objects.get(user=self.user)

    def test_profile_creation_signal(self):
        user = get_user_model().objects.create(email="proba@example.com", password="Test123!")
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_custom_user_creation_form_whit_valid_data(self):
        url = reverse("signup")
        form_data = {
            "email": "proba@example.com",
            "password1": "Test123!",
            "password2": "Test123!"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/')

    def test_custom_user_creation_form_whit_exists_email(self):
        form_data = {
            "email": "test@example.com",
            "password1": "Test123?",
            "password2": "Test123!"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(form.errors["email"],
                         ['A user with that email already exists.'])

    def test_custom_user_creation_form_whit_unmatched_fields(self):
        form_data = {
            "email": "test@example.com",
            "password1": "Test123?",
            "password2": "Test123!"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
        self.assertEqual(form.errors["password2"],
                         ["The two password fields didn't match."])

    def test_custom_user_creation_form_without_upper_leather(self):
        form_data = {
            "email": "test@example.com",
            "password1": "test123!",
            "password2": "test123!"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)
        self.assertEqual(form.errors["password1"],
                         ["Password must contain at least one uppercase letter."])

    def test_custom_user_creation_form_without_special_symbol(self):
        form_data = {
            "email": "test@example.com",
            "password1": "Test1234",
            "password2": "Test1234"
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)
        self.assertEqual(form.errors["password1"],
                         ["Password must contain at least one special character."])

    def test_profile_edit_form(self):
        self.assertEqual(self.profile.first_name, "")
        self.assertEqual(self.profile.last_name, "")
        self.assertEqual(self.profile.phone_number, "")
        self.assertEqual(self.profile.city, "")
        self.assertEqual(self.profile.address, None)

        form_data = {
            "first_name": "Updated",
            "last_name": "User",
            "phone_number": "1234567890",
            "city": "New York",
            "address": "456 Elm St"
        }
        form = ProfileEditForm(instance=self.profile, data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(self.profile.first_name, "Updated")
        self.assertEqual(self.profile.last_name, "User")
        self.assertEqual(self.profile.phone_number, "1234567890")
        self.assertEqual(self.profile.city, "New York")
        self.assertEqual(self.profile.address, "456 Elm St")

    def test_profile_edit_form_with_wrong_phone_number(self):
        self.assertEqual(self.profile.phone_number, "")

        form_data = {
            "first_name": "Updated",
            "last_name": "User",
            "phone_number": "123456789",
            "city": "New York",
            "address": "456 Elm St"
        }
        form = ProfileEditForm(instance=self.profile, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone_number'], ["Phone number must contain exactly 10 digits."])
        self.assertEqual(self.profile.phone_number, "")

    def test_profile_delete_form(self):
        self.assertTrue(get_user_model().objects.filter(email=self.user.email).exists())
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

        form = ProfileDeleteForm(instance=self.profile)
        form.delete_user()

        self.assertFalse(get_user_model().objects.filter(email='test@example.com').exists())
        self.assertFalse(UserProfile.objects.filter(user=self.user).exists())
