import os

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Creates a new API v1 module directory structure"

    def add_arguments(self, parser):
        parser.add_argument("module_name", type=str, help="Name of the module")

    def handle(self, *args, **options):
        module_name = options["module_name"].lower()
        module_path = os.path.join("api", "v1", module_name)
        test_path = os.path.join(module_path, "tests")

        if os.path.exists(module_path):
            raise CommandError(f"Module '{module_name}' already exists.")

        # Create directories
        os.makedirs(test_path, exist_ok=True)

        # Files to generate
        files = {
            os.path.join(module_path, "__init__.py"): "",
            os.path.join(
                module_path, "views.py"
            ): "from rest_framework.views import APIView\n",
            os.path.join(
                module_path, "serializers.py"
            ): "from rest_framework import serializers\n",
            os.path.join(
                module_path, "urls.py"
            ): "from django.urls import path\n\nurlpatterns = []\n",
            os.path.join(module_path, "services.py"): "",
            os.path.join(test_path, "__init__.py"): "",
        }

        for path, content in files.items():
            with open(path, "w") as f:
                f.write(content)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created module '{module_name}' at {module_path}"
            )
        )
