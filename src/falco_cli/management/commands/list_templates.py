# inspriation from https://noumenal.es/notes/tailwind/django-integration/
from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.utils import get_app_template_dirs


class Command(BaseCommand):
    help = "List all template files of the Django project."

    def handle(self, *_, **__):
        app_template_dirs = get_app_template_dirs("templates")
        setting_template_dirs = [Path(str(dir_)) for dir_ in settings.TEMPLATES[0]["DIRS"]]

        template_files = []
        for dir_ in [*app_template_dirs, *setting_template_dirs]:
            template_files.extend(self.list_template_files(dir_))

        self.stdout.write("\n".join(template_files))

    def list_template_files(self, template_dir: Path) -> list[str]:
        return [str(file_path) for file_path in Path(template_dir).rglob("*") if file_path.suffix in [".html", ".txt"]]
