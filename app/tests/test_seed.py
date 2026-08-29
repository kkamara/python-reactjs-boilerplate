from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from api.models import UserProfile

User = get_user_model()


class SeedCommandTests(TestCase):
    def test_seed_creates_demo_user_and_fake_users(self):
        out = StringIO()
        call_command("seed", "--users=5", stdout=out)

        # Demo user "jane" should exist and be the last created user
        self.assertTrue(User.objects.filter(username="jane").exists())
        jane = User.objects.get(username="jane")
        self.assertEqual(jane.email, "jane@example.com")
        self.assertEqual(jane.first_name, "Jane")
        self.assertEqual(jane.last_name, "Doe")
        self.assertTrue(jane.check_password("secret"))
        self.assertTrue(UserProfile.objects.filter(user=jane).exists())

        # Total users should be 5 (fake) + 1 (demo) = 6
        self.assertEqual(User.objects.count(), 6)
        self.assertEqual(UserProfile.objects.count(), 6)

        # Jane should have the highest ID and appear first in -id order
        first_user = User.objects.order_by("-id").first()
        self.assertEqual(first_user.id, jane.id)
        self.assertEqual(first_user.username, "jane")

    def test_seed_with_custom_password(self):
        out = StringIO()
        call_command("seed", "--users=2", "--password=custompass", stdout=out)

        jane = User.objects.get(username="jane")
        self.assertTrue(jane.check_password("custompass"))

    def test_seed_undo_deletes_seeded_users_and_keeps_superusers(self):
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="secretpassword",
        )
        User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="secretpassword",
            is_staff=True,
        )

        out = StringIO()
        call_command("seed", "--users=3", stdout=out)
        self.assertEqual(User.objects.count(), 6)  # admin + staff + 3 fake + jane

        call_command("seed", "--undo", stdout=out)
        self.assertEqual(User.objects.count(), 2)
        self.assertTrue(User.objects.filter(username="admin").exists())
        self.assertTrue(User.objects.filter(username="staff").exists())
        self.assertFalse(User.objects.filter(username="jane").exists())

    def test_repeated_seed_is_idempotent_for_demo_user(self):
        out = StringIO()
        call_command("seed", "--users=2", stdout=out)
        initial_count = User.objects.count()

        call_command("seed", "--users=2", stdout=out)
        # Jane is updated/reused, 2 additional fake users are created
        self.assertEqual(User.objects.count(), initial_count + 2)
