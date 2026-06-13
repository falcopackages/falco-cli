from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection
from falco_cli.management.base import exit_if_debug_false
from falco_cli.management.base import get_apps_dir
from falco_cli.management.commands.rm_migrations import Command as RmMigrationsCommand
from falco_cli.utils import simple_progress


class Command(BaseCommand):
    help = "Delete and recreate all migrations while keeping the database data."
    requires_migrations_checks = True

    def handle(self, *_, **__):
        exit_if_debug_false()
        # TODO: should stop if all current migrations are not applied
        apps_dir = get_apps_dir()
        RmMigrationsCommand.delete_migration_files(apps_dir=apps_dir)
        with simple_progress("Resetting migrations..."):
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM django_migrations")
            call_command("makemigrations")
            call_command("migrate", "--fake")
        self.stdout.write(self.style.SUCCESS("Done!"))
