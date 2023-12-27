import cappa
from falco.utils import run_in_shell
from rich import print as rich_print

make_superuser_code = """
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
    help="Make a superuser from some pre-defined django settings.",
    name="make-superuser",
)
class MakeSuperUser:
    def __call__(self):
        run_in_shell(make_superuser_code, eval_result=False)
        rich_print("[green]Superuser created successfully.")
