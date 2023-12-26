import cappa
from falco.utils import run_shell_command
from rich import print as rich_print

make_superuser_code = """
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()
email = getattr(settings, "SUPERUSER_EMAIL", "")
password = getattr(settings, "SUPERUSER_PASSWORD", "")
if not email or not password:
    raise ValueError("SUPERUSER_EMAIL and SUPERUSER_PASSWORD must be set in your settings file.")
if User.objects.filter(email=email).exists():
    raise ValueError("A superuser with this email already exists.")
user = User.objects.create_superuser(email=email)
user.set_password(password)
user.save()
"""


@cappa.command(
    help="Make a superuser from some pre-defined django settings.",
    name="make-superuser",
    description="""This command creates a superuser using the values of `SUPERUSER_EMAIL` and `SUPERUSER_PASSWORD` defined in your settings file.
""",
)
class MakeSuperUser:
    def __call__(self):
        run_shell_command(make_superuser_code, eval_result=False)
        rich_print("[green]Superuser created successfully.")
