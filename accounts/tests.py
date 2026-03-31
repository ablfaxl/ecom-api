from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user_persists_email_and_hashed_password(self):
        user = User.objects.create_user(
            email="person@example.com",
            password="secret-value",
        )
        user.refresh_from_db()
        self.assertEqual(user.email, "person@example.com")
        self.assertTrue(user.check_password("secret-value"))
        self.assertNotEqual(user.password, "secret-value")

    def test_create_user_requires_email(self):
        with self.assertRaisesMessage(ValueError, "Email is required"):
            User.objects.create_user(email="", password="x")

    def test_email_unique(self):
        User.objects.create_user(email="dup@example.com", password="a")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="dup@example.com", password="b")

    def test_create_superuser_sets_staff_and_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            password="admin-pass",
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_username_field_is_email(self):
        self.assertEqual(User.USERNAME_FIELD, "email")

    def test_user_str_uses_email(self):
        user = User.objects.create_user(email="u@example.com", password="p")
        self.assertEqual(str(user), "u@example.com")
