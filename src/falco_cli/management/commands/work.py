import importlib.util
import subprocess
from multiprocessing import Pool

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run every dev process needed in one command"

    def add_arguments(self, parser):
        parser.add_argument(
            "address",
            type=str,
            nargs="?",
            default="127.0.0.1:8000",
            help="Address to run the django server on",
        )
        parser.add_argument(
            "-p",
            "--plus",
            action="store_true",
            help="Run the server using runserver_plus",
        )

    def handle(self, *_, **options):
        address = options["address"]
        use_runserver_plus = options["plus"]
        commands = {
            "runserver": (
                "python -m django runserver_plus {address}"
                if use_runserver_plus
                else "python -m django runserver {address}"
            )
        }
        if "django_tailwind_cli" in settings.INSTALLED_APPS:
            commands["tailwind"] = f"python -m django tailwind watch"
        if "tailwind" in settings.INSTALLED_APPS:
            commands["tailwind"] = f"python -m django tailwind start"
        if "django_q" in settings.INSTALLED_APPS:
            commands["qcluster"] = f"python -m django qcluster"

        try:
            run_db_worker = settings.TASKS["default"]["BACKEND"] in [
                "django_tasks.backends.database.DatabaseBackend",
                "django.tasks.backends.database.DatabaseBackend",
            ]
        except (AttributeError, KeyError):
            run_db_worker = False

        if run_db_worker:
            commands["worker"] = f"python -m django db_worker -v 3"

        commands["runserver"] = commands["runserver"].format(address=address)

        call_command("migrate")
        if importlib.util.find_spec("honcho"):
            self.run_with_honcho(commands)
        else:
            self.run_with_multiprocess(commands)

    @classmethod
    def run_with_multiprocess(cls, commands: dict):
        with Pool(processes=len(commands)) as pool:
            try:
                pool.map(subprocess.run, [cmd.split() for cmd in commands.values()])
            except KeyboardInterrupt:
                pool.terminate()
            finally:
                pool.close()
                pool.join()

    @classmethod
    def run_with_honcho(cls, commands: dict):
        from honcho.manager import Manager

        manager = Manager()
        for name, cmd in commands.items():
            manager.add_process(name, cmd)
        try:
            manager.loop()
        finally:
            manager.terminate()
