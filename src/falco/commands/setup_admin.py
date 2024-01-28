import cappa
from falco.utils import run_in_shell
from rich import print as rich_print
from falco.utils import ShellCodeError

admin_setup_code = """
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()
settings_dict = {k: getattr(settings, k) for k in dir(settings) if k.isupper()}

def arg_name_from_settings_name(settings_name):
    _, *n = settings_name.lower().split("_")
    return "_".join(n)

superuser_settings = {
    arg_name_from_settings_name(key): value
    for key, value in settings_dict.items()
    if key.startswith("SUPERUSER_")
}
password = superuser_settings.pop("password", None)
if not password:
    raise ValueError("SUPERUSER_PASSWORD must be set in your settings file.")

if User.objects.filter(**superuser_settings).exists():
    raise ValueError("A superuser with the settings configured already exists.")

user = User.objects.create_superuser(**superuser_settings)
user.set_password(password)
user.save()
"""


@cappa.command(
    help="Create a superuser from some pre-defined django settings.",
    name="setup-admin",
)
class SetupAdmin:
    def __call__(self):
        try:
            run_in_shell(admin_setup_code, eval_result=False)
        except ShellCodeError as e:
            msg = str(e).split("\n")[-2]
            raise cappa.Exit(msg, code=1) from e
        rich_print("[green]Superuser created successfully.")
