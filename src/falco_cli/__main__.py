import cappa
from falco_cli.commands import Htmx
from falco_cli.commands import HtmxExtension
from falco_cli.commands import ModelCRUD
from falco_cli.commands import ResetMigrations
from falco_cli.commands import RmMigrations
from falco_cli.commands import StartApp
from falco_cli.commands import StartProject
from falco_cli.commands import SyncDotenv
from falco_cli.commands import UpdateProject
from falco_cli.commands import Work


@cappa.command(
    help="Enhance your Django developer experience: CLI and Guides for the Modern Django Developer.",
)
class Falco:
    subcommand: cappa.Subcommands[
        StartProject
        | UpdateProject
        | StartApp
        | ModelCRUD
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
