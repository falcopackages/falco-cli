import cappa

from .fmt import Fmt
from .start_project import StartProject
from .sync_dotenv import SyncDotenv
from .update_project import UpdateProject


@cappa.command(
    help="Enhance your Django developer experience: CLI and Guides for the Modern Django Developer.",
)
class Falco:
    subcommand: cappa.Subcommands[StartProject | UpdateProject | Fmt | SyncDotenv]


def main():
    cappa.invoke(Falco)


if __name__ == "__main__":
    main()
