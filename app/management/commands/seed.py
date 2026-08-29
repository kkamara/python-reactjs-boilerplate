import re

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from api.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the database with fake users and demo data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=30,
            help="Number of fake users to generate (default: 30)",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="secret",
            help="Default password for seeded users (default: secret)",
        )
        parser.add_argument(
            "--undo",
            action="store_true",
            help="Undo database seed by deleting seeded users",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Alias for --undo: remove seeded users",
        )

    def handle(self, *args, **options):
        undo = options.get("undo") or options.get("clear")
        count = options.get("users", 30)
        password = options.get("password", "secret")

        if undo:
            self.undo_seed()
            return

        self.seed_users(count, password)

    def _sanitize_username(self, raw_username: str, suffix: int) -> str:
        clean = re.sub(r"[^\w.@+-]", "", raw_username).lower()
        if len(clean) < 3:
            clean = f"user{clean}"
        clean = clean[:14]
        return f"{clean}{suffix:04d}"[:19]

    def seed_users(self, count: int, password: str):
        fake = Faker()
        created_count = 0

        self.stdout.write(self.style.WARNING("Starting database seeding..."))

        with transaction.atomic():
            # Seed fake users first
            for i in range(count):
                first_name = fake.first_name()[:19]
                last_name = fake.last_name()[:19]
                email = fake.unique.email()[:100]

                # Ensure unique valid username between 3 and 19 characters, excluding "jane"
                username_base = fake.user_name()
                username = self._sanitize_username(username_base, i + 1)
                attempts = 0
                while (
                    username == "jane"
                    or User.objects.filter(username=username).exists()
                ) and attempts < 100:
                    attempts += 1
                    username = self._sanitize_username(
                        f"{fake.user_name()}{attempts}", i + 1
                    )

                # Ensure unique email, excluding "jane@example.com"
                email_attempts = 0
                while (
                    email.lower() == "jane@example.com"
                    or User.objects.filter(email=email).exists()
                ) and email_attempts < 100:
                    email_attempts += 1
                    email = f"user_{i + 1}_{fake.unique.email()}"[:100]

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                )
                UserProfile.objects.get_or_create(user=user)
                created_count += 1

            # Seed demo user Jane Doe last so that she has the highest ID and appears first in -id queries
            demo_user, created = User.objects.get_or_create(
                username="jane",
                defaults={
                    "email": "jane@example.com",
                    "first_name": "Jane",
                    "last_name": "Doe",
                },
            )
            demo_user.set_password(password)
            demo_user.first_name = "Jane"
            demo_user.last_name = "Doe"
            demo_user.email = "jane@example.com"
            demo_user.save()
            UserProfile.objects.get_or_create(user=demo_user)

            if created:
                created_count += 1
                self.stdout.write(
                    f"Created demo user: {demo_user.username} ({demo_user.email})"
                )
            else:
                self.stdout.write(
                    f"Updated demo user: {demo_user.username} ({demo_user.email})"
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded {created_count} user(s) into the database."
            )
        )

    def undo_seed(self):
        self.stdout.write(self.style.WARNING("Reverting database seeding..."))

        with transaction.atomic():
            # Delete non-staff, non-superuser accounts
            _deleted_profiles, _ = UserProfile.objects.filter(
                user__is_staff=False, user__is_superuser=False
            ).delete()
            deleted_users, _ = User.objects.filter(
                is_staff=False, is_superuser=False
            ).delete()

        self.stdout.write(
            self.style.SUCCESS(f"Successfully deleted {deleted_users} seeded user(s).")
        )
