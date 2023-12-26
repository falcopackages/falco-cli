import cappa
from falco.commands import Htmx
from falco.commands import HtmxExtension
from falco.commands import InstallCrudUtils
from falco.commands import MakeSuperUser
from falco.commands import ModelCRUD
from falco.commands import ResetMigrations
from falco.commands import RmMigrations
from falco.commands import StartProject
from falco.commands import SyncDotenv
from falco.commands import Work


@cappa.command(
    help="Enhance your Django developer experience: CLI and Guides for the Modern Django Developer.",
)
class Falco:
    subcommand: cappa.Subcommands[
        StartProject
        | ModelCRUD
        | InstallCrudUtils
        | Htmx
        | HtmxExtension
        | Work
        | SyncDotenv
        | RmMigrations
        | ResetMigrations
        | MakeSuperUser
    ]


def main():
    cappa.invoke(Falco)


if __name__ == "__main__":
    main()
