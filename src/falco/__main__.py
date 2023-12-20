import cappa
from falco.commands import Htmx
from falco.commands import HtmxExtension
from falco.commands import MakeSuperUser
from falco.commands import ModelCRUD
from falco.commands import RmMigrations
from falco.commands import StartProject
from falco.commands import SyncDotenv
from falco.commands import Work


@cappa.command(
    help="Initialize a new django project using the falco project template.",
    description="""This is a wrapper around the django-admin startproject command using my custom project template at
    https://github.com/Tobi-De/falco. This cli also includes some additional commands to make setting up
    a new project faster.
    """,
)
class Falco:
    subcommand: cappa.Subcommands[
        StartProject | ModelCRUD | Htmx | HtmxExtension | Work | SyncDotenv | RmMigrations | MakeSuperUser
    ]


def main():
    cappa.invoke(Falco)


if __name__ == "__main__":
    main()
