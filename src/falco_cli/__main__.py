from importlib.metadata import version

import cappa

from .fmt import Fmt
from .start_project import StartProject
from .update_project import UpdateProject


@cappa.command(
    help="Enhance your Django developer experience: CLI and Guides for the Modern Django Developer.",
)
class Falco:
    subcommand: cappa.Subcommands[StartProject | UpdateProject | Fmt]


def main():
    cappa.invoke(Falco, version=version("falco-cli"))


if __name__ == "__main__":
    main()
