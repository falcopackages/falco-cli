import cappa
from falco.commands import Htmx
from falco.commands import HtmxExtension
from falco.commands import InstallCrudUtils
from falco.commands import ModelCRUD
from falco.commands import ResetMigrations
from falco.commands import RmMigrations
from falco.commands import StartApp
from falco.commands import StartProject
from falco.commands import SyncDotenv
from falco.commands import Work


@cappa.command(
    help="Enhance your Django developer experience: CLI and Guides for the Modern Django Developer.",
)
class Falco:
    subcommand: cappa.Subcommands[
        StartProject
        | StartApp
        | ModelCRUD
        | InstallCrudUtils
        | Htmx
        | HtmxExtension
        | Work
        | SyncDotenv
        | RmMigrations
        | ResetMigrations
    ]


def main():
    cappa.invoke(Falco)


if __name__ == "__main__":
    main()


# runno=ing setup-admin two times in a row result in an ugly erro message
# maybe crud should take care of the migrations and migrate for the model
